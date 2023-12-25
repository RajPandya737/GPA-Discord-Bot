import discord
from discord.ext import commands
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

connection_string = os.getenv('DB_LINK')

client = MongoClient(connection_string)
database = client["UserDB"]


collection_name = 'users'
collection = database[collection_name]


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name='addUser')
async def addUser(ctx):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if not user_exists:
        new_entry = {"userid": user_id}
        collection.insert_one(new_entry)
        await ctx.send(f"You have been added!")
    else:
        await ctx.send(f"You already exist in the collection!")
        
        
@bot.command(name='addCourse')
async def add_course(ctx, course):
    user_id = ctx.author.id

    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        if 'courses' not in user_exists:
            user_exists['courses'] = []

        if course not in user_exists['courses']:
            user_exists['courses'].append(course)
            user_exists[course] = {}
            collection.update_one(
                {"userid": user_id},
                {"$set": {"courses": user_exists['courses'], course: {}}}
            )

            await ctx.send(f"Course '{course}' added to your profile.")
        else:
            await ctx.send(f"Course '{course}' already exists in your profile.")
    else:
        await ctx.send("User does not exist. To add a user, call '$addUser'.")

@bot.command(name='removeCourse')
async def remove_course(ctx, course):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})
    if user_exists:
        courses = user_exists.get('courses', [])
        if course in courses:
            courses.remove(course)
            del user_exists[course]

            try:
                collection.update_one({"userid": user_id}, {"$set": {"courses": courses}})
                await ctx.send(f"Course '{course}' removed from your profile.")
            except Exception as e:
                await ctx.send(f"Error updating document: {e}")
        else:
            await ctx.send(f"Course '{course}' does not exist in your profile.")
    else:
        await ctx.send("User does not exist. To add a user, call '$addUser'.")

@bot.command(name='addAssignment')
async def add_assignment(ctx, course, assignment, grade, weight):
    user_id = ctx.author.id

    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])

        if course in courses:
            user_exists[course][assignment] = {'grade': grade, 'weight': weight}
            collection.update_one(
                {"userid": user_id},
                {"$set": {f"{course}.{assignment}": {'grade': grade, 'weight': weight}}}
            )

            await ctx.send(f"Assignment '{assignment}' added to the '{course}' course")
        else:
            await ctx.send(f"Course '{course}' does not exist. To add a course, type '$addCourse'")
    else:
        await ctx.send(f"User does not exist. To add a user, type '$addUser'.")




@bot.command(name='removeAssignment')
async def remove_assignment(ctx, course, assignment):
    user_id = ctx.author.id

    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])

        if course in courses:
            assignments = user_exists.get(course, {})
            if assignment in assignments:
                del assignments[assignment]

                collection.update_one(
                    {"userid": user_id},
                    {"$unset": {f"{course}.{assignment}": ""}}
                )

                await ctx.send(f"Assignment '{assignment}' removed for {course} ")
            else:
                await ctx.send(f"Assignment '{assignment}' does not exist for {course}")
        else:
            await ctx.send(f"Course '{course}' does not exist. To add a course, type '$addCourse'")
    else:
        await ctx.send(f"User does not exist. To add a user, type '$addUser'.")

@bot.command(name='removeAllAssignments')
async def remove_all_assignments(ctx, course):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])
        if course in courses:
            user_exists[course] = {}  
            try:
                collection.update_one({"userid": user_id}, {"$unset": {f"{course}": ""}})
                await ctx.send(f"All assignments removed for '{course}'.")
            except Exception as e:
                await ctx.send(f"Error updating document: {e}")
        else:
            await ctx.send(f"Course '{course}' does not exist.")
    else:
        await ctx.send("User does not exist. To add a user, type '$addUser'.")


def convert_to_12_scale(percentage):
    if percentage >= 90:
        return 12
    elif 85 <= percentage < 90:
        return 11
    elif 80 <= percentage < 85:
        return 10
    elif 77 <= percentage < 80:
        return 9
    elif 73 <= percentage < 77:
        return 8
    elif 70 <= percentage < 73:
        return 7
    elif 67 <= percentage < 70:
        return 6
    elif 63 <= percentage < 67:
        return 5
    elif 60 <= percentage < 63:
        return 4
    elif 57 <= percentage < 60:
        return 3
    elif 53 <= percentage < 57:
        return 2
    elif 50 <= percentage < 53:
        return 1
    else:
        return 0
    
    
@bot.command(name='calculateGrade')
async def calculate_grade(ctx, course):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])
        if course in courses:
            assignments = user_exists[course]
            total_weighted_grade = 0
            total_weight = 0

            for assignment, details in assignments.items():
                grade = details.get('grade', 0)
                weight = details.get('weight', 0)
                total_weighted_grade += int(grade) * int(weight)
                total_weight += int(weight)

            if total_weight > 0:
                average_grade = total_weighted_grade / total_weight
                grade_message = f"Calculated average grade for '{course}': {average_grade:.2f} ({convert_to_12_scale(average_grade)})"
                await ctx.send(grade_message)
                return average_grade
            else:
                await ctx.send(f"No assignments with weights found for '{course}'.")
                return None
        else:
            await ctx.send(f"Course '{course}' does not exist.")
            return None
    else:
        await ctx.send("User does not exist. To add a user, type '$addUser'")
        return None



@bot.command(name='wantedGrade')
async def wanted_grade(ctx, course, target_grade):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])
        if course in courses:
            assignments = user_exists[course]
            total_weighted_grade = 0
            total_weight = 0
            for assignment, details in assignments.items():
                grade = details.get('grade', 0)
                weight = details.get('weight', 0)
                total_weighted_grade += grade * weight
                total_weight += weight

            remaining_grade = round((float(target_grade) * 100 - total_weighted_grade) / (100 - total_weight), 2)
            await ctx.send(f"Remaining grade needed for '{course}' to achieve a target grade of {target_grade}: {remaining_grade}")
        else:
            await ctx.send(f"Course '{course}' does not exist.")
    else:
        await ctx.send("User does not exist. To add a user, type '$addUser'.")
        
@bot.command(name='listCourses')
async def list_courses(ctx):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})
    
    if user_exists:
        courses = user_exists.get('courses', [])
        if len(courses) > 0:
            await ctx.send(f"Your courses are: {', '.join(courses)}")
        else:
            await ctx.send("You have no courses.")
            
            
@bot.command(name='removeAllCourses')
async def remove_all_courses(ctx):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        try:
            collection.update_one({"userid": user_id}, {"$unset": {"courses": ""}})
            await ctx.send("All courses removed for the user.")
        except Exception as e:
            await ctx.send(f"Error updating document: {e}")
    else:
        await ctx.send("User does not exist. To add a user, type '$addUser'.")

@bot.command(name='removeUser')
async def remove_user(ctx):
    user_id = ctx.author.id
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        try:
            collection.delete_one({"userid": user_id})
            await ctx.send("User removed from the database.")
        except Exception as e:
            await ctx.send(f"Error deleting document: {e}")
    else:
        await ctx.send("User does not exist. To add a user, type '$addUser'.")


bot.run(os.getenv('TOKEN'))

# wanted features:

#1. overall grade (all courses)
import discord
from discord.ext import commands
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

dotenv.load_dotenv()

intents = discord.Intents.all() 
client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print('Bot is ready.')
    

@client.command()
async def addCourse(ctx, course):
    await ctx.send(f'Adding course {course} for user {user_id}')
    pass

    
    


def addUser():
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)
            
    user_exists = any(entry.get('userid') == user_id for entry in data)

    if not user_exists:
        new_entry = {"userid": user_id}
        data.append(new_entry)

        # Write the updated JSON data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)

        print(f"Userid '{user_id}' added to the JSON file.")
    else:
        print(f"Userid '{user_id}' already exists in the JSON file.")    

def addCourse(course):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)
            
    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                if course not in entry.get('courses'):
                    entry['courses'].append(course)
                break

        # Write the updated JSON data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)

        print(f"Course '{course}' added to the JSON file.")
    else:
        print(f"User does not exist. To add a user type '$addUser'")
        
def removeCourse(course):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)

    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                courses = entry.get('courses', [])
                if course in courses:
                    entry['courses'].remove(course)
                    del entry[course]  # Remove the course entry from the dictionary
                    print(f"Course '{course}' removed for user '{user_id}'.")
                else:
                    print(f"Course '{course}' does not exist.")
                break

        # Write the updated JSON data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)
    else:
        print(f"User does not exist. To add a user, type '$addUser'")

# Example usage:
# removeCourse('math')


def addAssignment(course, assignment, grade, weight):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)
            
    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                courses = entry.get('courses', [])  # Default to an empty list if 'courses' is not present
                if course in courses:
                    # Check if the 'course' key exists in the entry, if not, create an empty dictionary for it
                    if course not in entry:
                        entry[course] = {}
                    entry[course][assignment] = {'grade': grade, 'weight': weight}
                else:
                    print(f"Course '{course}' does not exist. To add a course type '$addCourse'")
                    return  # Exit the function if the course doesn't exist

        # Write the updated JSON data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)

        print(f"Assignment '{assignment}' added to the '{course}' course for user '{user_id}'.")
    else:
        print(f"User does not exist. To add a user type '$addUser'")


def removeAssignment(course, assignment):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)

    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                courses = entry.get('courses', [])
                if course in courses and course in entry:
                    if assignment in entry[course]:
                        del entry[course][assignment]
                        print(f"Assignment '{assignment}' removed from the '{course}' course for user '{user_id}'.")
                    else:
                        print(f"Assignment '{assignment}' does not exist for the '{course}' course.")
                else:
                    print(f"Course '{course}' does not exist. To add a course, type '$addCourse'")
                    return  # Exit the function if the course doesn't exist

        # Write the updated JSON data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)
    else:
        print(f"User does not exist. To add a user, type '$addUser'")

def calculateGrade(course):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)

    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                courses = entry.get('courses', [])
                if course in courses and course in entry:
                    assignments = entry[course]
                    total_weighted_grade = 0
                    total_weight = 0

                    for assignment, details in assignments.items():
                        grade = details.get('grade', 0)
                        weight = details.get('weight', 0)
                        total_weighted_grade += grade * weight
                        total_weight += weight

                    if total_weight > 0:
                        average_grade = total_weighted_grade / total_weight
                        print(f"Calculated average grade for '{course}': {average_grade:.2f}")
                        return average_grade
                    else:
                        print(f"No assignments with weights found for '{course}'.")
                        return None
                else:
                    print(f"Course '{course}' does not exist.")
                    return None
    else:
        print(f"User does not exist. To add a user, type '$addUser'")
        return None


def wantedGrade(course, target_grade):
    user_id = 'jar'
    with open('data.json', 'r') as file:
        data = json.load(file)

    user_exists = any(entry.get('userid') == user_id for entry in data)

    if user_exists:
        for entry in data:
            if entry.get('userid') == user_id:
                courses = entry.get('courses', [])
                if course in courses and course in entry:
                    assignments = entry[course]
                    total_weighted_grade = 0
                    total_weight = 0

                    for assignment, details in assignments.items():
                        grade = details.get('grade', 0)
                        weight = details.get('weight', 0)
                        total_weighted_grade += grade * weight
                        total_weight += weight
                    rest = round((target_grade * 100 - total_weighted_grade) / (100 - total_weight), 2)
                    print(rest)
                else:
                    print(f"Course '{course}' does not exist.")
    else:
        print(f"User does not exist. To add a user, type '$addUser'")
# Example usage:
# calculateGrade('math')


addCourse('math')
addAssignment('math', 'test', 90, 10)
addAssignment('math', 'test2', 95, 45)
addAssignment('math', 'test3', 30, 30)
calculateGrade('math')
wantedGrade('math', 20)

# client.run(os.getenv('TOKEN'))

# wanted features:

# 1. add course
# 2. remove course
# 3. list courses
# 4. calculate gpa
# 5. info about a course (gpa)
# 6. Mark needed to get x%
# 7. add assignment mark
# 8. remove assignment mark
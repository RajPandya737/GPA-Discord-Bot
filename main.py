import discord
from discord.ext import commands
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

dotenv.load_dotenv()

connection_string = os.getenv('DB_LINK')

client = MongoClient(connection_string)
database = client["UserDB"]


collection_name = 'users'
collection = database[collection_name]


intents = discord.Intents.all() 
client = commands.Bot(command_prefix='$', intents=intents)


def addUser():
    user_id = 'jar'
    user_exists = collection.find_one({"userid": user_id})

    if not user_exists:
        new_entry = {"userid": user_id}
        collection.insert_one(new_entry)

        print(f"Userid '{user_id}' added to the MongoDB collection.")
    else:
        print(f"Userid '{user_id}' already exists in the MongoDB collection.")

def addCourse(course):
    user_id = 'jar'

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

            print(f"Course '{course}' added to the MongoDB collection.")
        else:
            print(f"Course '{course}' already exists.")
    else:
        print(f"User does not exist. To add a user, call 'addUser'.")

def removeCourse(course):
    user_id = 'jar'
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])

        if course in courses:
            courses.remove(course)
            del user_exists[course]

            try:
                collection.update_one({"userid": user_id}, {"$set": {"courses": courses}})
                print(f"Course '{course}' removed for user '{user_id}'.")
            except Exception as e:
                print(f"Error updating document: {e}")
        else:
            print(f"Course '{course}' does not exist.")
    else:
        print(f"User does not exist. To add a user, call 'addUser'.")

# Example usage:



def addAssignment(course, assignment, grade, weight):
    user_id = 'jar'
    user_exists = collection.find_one({"userid": user_id})

    if user_exists:
        courses = user_exists.get('courses', [])

        if course in courses:
            user_exists[course][assignment] = {'grade': grade, 'weight': weight}
            collection.update_one(
                {"userid": user_id},
                {"$set": {f"{course}.{assignment}": {'grade': grade, 'weight': weight}}}
            )

            print(f"Assignment '{assignment}' added to the '{course}' course for user '{user_id}'.")
        else:
            print(f"Course '{course}' does not exist. To add a course type '$addCourse'")
    else:
        print(f"User does not exist. To add a user type '$addUser'")
    return



def removeAssignment(course, assignment):
    user_id = 'jar'
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

                print(f"Assignment '{assignment}' removed for the '{course}' course for user '{user_id}'.")
            else:
                print(f"Assignment '{assignment}' does not exist for the '{course}' course.")
        else:
            print(f"Course '{course}' does not exist. To add a course, type '$addCourse'")
    else:
        print(f"User does not exist. To add a user, type '$addUser'")
    return

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
    
    
def calculateGrade(course):
    user_id = 'jar'
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

            if total_weight > 0:
                average_grade = total_weighted_grade / total_weight
                print(f"Calculated average grade for '{course}': {average_grade:.2f} ({convert_to_12_scale(average_grade)})")
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
            remaining_grade = round((target_grade * 100 - total_weighted_grade) / (100 - total_weight), 2)
            print("Remaining grade needed: ", remaining_grade)
        else:
            print(f"Course '{course}' does not exist.")
    else:
        print(f"User does not exist. To add a user, type '$addUser'")


addCourse('math')
addAssignment('math', 'test', 80, 25)
addAssignment('math', 'test2', 90, 25)
calculateGrade('math')
wantedGrade('math', 90)


# addAssignment('math', 'test', 90, 10)
# addAssignment('math', 'test2', 95, 45)
# addAssignment('math', 'test3', 30, 30)
# calculateGrade('math')
# wantedGrade('math', 20)


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
import discord
from discord.ext import commands
import dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

intents = discord.Intents.all() 
client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print('Bot is ready.')
    

@client.command()
async def addCourse(ctx, course):
    user_id = str(ctx.author.id)
    await ctx.send(f'Adding course {course} for user {user_id}')
    
    
client.run(os.getenv('TOKEN'))

# wanted features:

# 1. add course
# 2. remove course
# 3. list courses
# 4. calculate gpa
# 5. info about a course (gpa)
# 6. Mark needed to get x%
# 7. add assignment mark
# 8. remove assignment mark
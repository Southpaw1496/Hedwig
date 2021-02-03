import discord
from discord.ext import commands
from discord import Embed, Colour
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
from os import environ
from discord import Intents
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix='!', intents=intents)



sqliteConnection = sqlite3.connect("Hedwig.db")
sqliteCursor = sqliteConnection.cursor()
sqliteCursor.execute("CREATE TABLE IF NOT EXISTS channels (username TEXT, userID INTEGER, channel_id INTEGER)")

@client.event
async def on_ready():
    print("Bot Online")

@client.event
async def on_message(message):
    if message.author == client.user: return 
    if not message.guild:
        userID = message.author.id
        username = message.author.name 
        guild = client.get_guild(int(environ.get("GUILD")))
        print(guild)
        StoredChannelID = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
        if StoredChannelID == []:
            category = guild.get_channel(int(environ.get("CATEGORY")))
            channel = await guild.create_text_channel(f'{username}', category=category)
            channel_id = channel.id
            sqliteCursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (username, userID, channel_id))
            sqliteConnection.commit()
            await channel.send(message.content)
        else:
            channel = client.get_channel(StoredChannelID[0][0])
            await channel.send(message.content)
    else:
        channel = message.channel
        channel_id = channel.id
        userID = sqliteCursor.execute("SELECT userID FROM channels WHERE channel_id = ?",(channel_id,)).fetchall()
        if userID == []: return
        else:
            user = client.get_user(userID[0][0])

            await user.send(message.content)

            
             

client.run(environ.get("TOKEN"))

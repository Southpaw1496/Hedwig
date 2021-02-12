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
guild = client.get_guild(int(environ.get("GUILD")))



sqliteConnection = sqlite3.connect("Hedwig.db")
sqliteCursor = sqliteConnection.cursor()
sqliteCursor.execute("CREATE TABLE IF NOT EXISTS channels (username TEXT, userID INTEGER, channel_id INTEGER)")

@client.event
async def on_ready():
    print("Bot Online")

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user or message.content.startswith("!"): return
    guild = client.get_guild(int(environ.get("GUILD"))) 
    if not message.guild:
        userID = message.author.id
        guild = client.get_guild(int(environ.get("GUILD")))
        username = message.author.name 
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
            if channel.category == int(environ.get("CATEGORY_ARCHIVE")):
                await channel.edit(category=category)
            await channel.send(message.content)
    else:
        channel = message.channel
        channel_id = channel.id
        userID = sqliteCursor.execute("SELECT userID FROM channels WHERE channel_id = ?",(channel_id,)).fetchall()
        if userID == []: return
        else:
            user = client.get_user(userID[0][0])
            if message.channel.category.id == int(environ.get("CATEGORY_ARCHIVE")):
                category = guild.get_channel(int(environ.get("CATEGORY")))
                await message.channel.edit(category=category)
            await user.send(message.content)

@client.event
async def on_guild_channel_delete(channel):
    channel_id = channel.id
    sqliteCursor.execute("DELETE FROM channels WHERE channel_id=?", (channel_id,))
    sqliteConnection.commit()
@client.command()
async def archive(context):
    guild = client.get_guild(int(environ.get("GUILD")))
    category = guild.get_channel(int(environ.get("CATEGORY_ARCHIVE")))
    await context.channel.edit(category=category)
    await context.channel.send("This channel has been archived")

@client.command()
async def message(context, username=None):
    guild = client.get_guild(int(environ.get("GUILD")))
    if username == None:
        await context.channel.send("Error: Username/ID is a required command argument")
        return
    elif message == None:
        await context.channel.send("Error: You need to send a message to send to the selected user")
        return
    elif username.isdecimal()  == True:
        user = client.get_user(int(username))
    elif username.isdecimal() == False:
        user = guild.get_member_named(username)
    userID = user.id
    if user == None:
            await context.channel.send("Couldn't find the user in this guild")
    else:
        stored_channel_id = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
        if stored_channel_id == []:
            category = guild.get_channel(int(environ.get("CATEGORY")))
            channel = await guild.create_text_channel(f'{user.name}', category=category)
            channel_id = channel.id
            sqliteCursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (username, userID, channel_id))
            sqliteConnection.commit()
            await context.channel.send(f"Created channel {channel.mention} which is connected to {user.mention}. Remember to identify yourself in your first message!")
        else:
            await context.channel.send("Error: This user is already linked to a channel. If you can't find it, look in your archive category")
        
    

client.run(environ.get("TOKEN"))

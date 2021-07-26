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
    if message.author == client.user or message.guild != None: return 
    else:
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
            finalMessage = f"**{message.author}:** {message.content}"
            await channel.send(finalMessage)
        
        else:
            channel = client.get_channel(StoredChannelID[0][0])
            if channel.category == int(environ.get("CATEGORY_ARCHIVE")):
                await channel.edit(category=category)
            finalMessage = f"**{message.author}:** {message.content}"
            await channel.send(finalMessage)

@client.event
async def on_message_edit(before, after):
    if before.author == client.user or before.guild != None or before.content == after.content: return 
    else:
        userID = before.author.id
        guild = client.get_guild(int(environ.get("GUILD")))
        category = guild.get_channel(int(environ.get("CATEGORY")))
        StoredChannelID = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
        channel = client.get_channel(StoredChannelID[0][0])
        if channel.category == int(environ.get("CATEGORY_ARCHIVE")):
            await channel.edit(category=category)
        finalMessage = f"**{before.author} edited their message:** \n `A:` {before.content} \n `B:` {after.content}"
        await channel.send(finalMessage)


@client.command(aliases=["r"])
async def reply(context, *, message):
    channel = context.channel
    channel_id = channel.id
    userID = sqliteCursor.execute("SELECT userID FROM channels WHERE channel_id = ?",(channel_id,)).fetchall()
    if userID == []: return
    else:
        user = client.get_user(userID[0][0])
        if context.channel.category.id == int(environ.get("CATEGORY_ARCHIVE")):
            category = guild.get_channel(int(environ.get("CATEGORY")))
            await context.channel.edit(category=category)
        publicDisplayMessage = f"**{context.author.display_name}:** {message}"
        await context.message.delete()
        await channel.send(publicDisplayMessage)
        await user.send(message)

@client.event
async def on_guild_channel_delete(channel):
    channel_id = channel.id
    sqliteCursor.execute("DELETE FROM channels WHERE channel_id=?", (channel_id,))
    sqliteConnection.commit()
@client.command()
async def archive(context):
    guild = client.get_guild(int(environ.get("GUILD")))
    category = guild.get_channel(int(environ.get("CATEGORY_ARCHIVE")))
    if context.channel.category_id != int(environ.get("CATEGORY")):
        print(f"User {context.author} tried to archive a channel that is not in your modmail category")
        return
    await context.channel.edit(category=category)
    await context.channel.send("This channel has been archived")

@client.command()
async def message(context, username=None, *, message=None):
    guild = client.get_guild(int(environ.get("GUILD")))
    roleList = [role.id for role in context.author.roles]
    if not int(environ.get("MESSAGE_ROLE")) in roleList: return 
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

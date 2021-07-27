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
allowedRoles = environ.get("ALLOWED_ROLES").split(", ")
for i in range(0, len(allowedRoles)):
    roleName = allowedRoles[i]
    allowedRoles[i] = int(roleName)

def roleCheck(context):
    userRoles = [role.id for role in context.author.roles]
    if context.guild.owner == context.author: return True
    else:
        for r in userRoles:
            if r in allowedRoles:
                return True
        return False

async def userLink(user, guild):
    userID = user.id
    stored_channel_id = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
    if stored_channel_id == []:
        category = guild.get_channel(int(environ.get("CATEGORY")))
        channel = await guild.create_text_channel(f'{user.name}', category=category)
        channel_id = channel.id
        sqliteCursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (user.name, userID, channel_id))
        sqliteConnection.commit()

def linkCheck(userID):
    stored_channel_id = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
    if stored_channel_id == []:
        return False
    return True

async def usernameParser(context, guild, username):
    if username == None:
        await context.channel.send("⚠️ **Error**: Username/ID is a required command argument")
        return
    elif username.isdecimal()  == True:
        user = client.get_user(int(username))
    elif username.isdecimal() == False:
        user = guild.get_member_named(username)
    if user == None:
            await context.channel.send("⚠️ **Error**: Couldn't find the user in this guild")
            return
    return user

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
        category = guild.get_channel(int(environ.get("CATEGORY")))
        StoredChannelID = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(userID,)).fetchall()
        if StoredChannelID == []:
            channel = await guild.create_text_channel(f'{username}', category=category)
            channel_id = channel.id
            sqliteCursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (username, userID, channel_id))
            sqliteConnection.commit()
            finalMessage = f"**{message.author}:** {message.content}"
            await message.author.send("✅ Your message has been received, we'll get back to you as soon as possible")
            await channel.send(f"**⚙️ {client.user.display_name}:** ✅ Your message has been received, we'll get back to you as soon as possible")
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

@client.event
async def on_guild_channel_delete(channel):
    channel_id = channel.id
    sqliteCursor.execute("DELETE FROM channels WHERE channel_id=?", (channel_id,))
    sqliteConnection.commit()


@client.command(aliases=["r"])
async def reply(context, *, message):
    guild = client.get_guild(int(environ.get("GUILD")))
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

@client.command()
async def archive(context):
    guild = client.get_guild(int(environ.get("GUILD")))
    category = guild.get_channel(int(environ.get("CATEGORY_ARCHIVE")))
    if context.channel.category_id != int(environ.get("CATEGORY")):
        print(f"User {context.author} tried to archive a channel that is not in your modmail category")
        return
    await context.channel.edit(category=category)
    await context.channel.send("✅ This channel has been archived")

@client.command()
async def link(context, username):
    if roleCheck(context=context) == False:
        return
    guild = client.get_guild(int(environ.get("GUILD")))
    user = await usernameParser(context=context, username=username,guild=guild)
    if user == None:
        return
    sqliteCursor.execute("DELETE FROM channels WHERE userID=?", (user.id,))
    sqliteCursor.execute("INSERT INTO channels VALUES (?, ?, ?)", (username, user.id, context.channel.id))
    sqliteConnection.commit()
    await context.channel.send(f"✅ This channel is now linked to {user.mention}. Use !unlink to unlink it")

@client.command()
async def unlink(context):
    if roleCheck(context=context) == False:
        return
    channelID = sqliteCursor.execute("SELECT channel_id FROM channels WHERE channel_id = ?",(context.channel.id,)).fetchall()
    if channelID == None:
        await context.channel.send("⚠️ **Error:** This channel is not linked to a user")
    else:
        sqliteCursor.execute("DELETE FROM channels WHERE channel_id = ?", (context.channel.id,))
        sqliteConnection.commit()
        await context.channel.send("✅ This channel has been unlinked")

@client.command()
async def message(context, username=None, *, message=None):
    guild = client.get_guild(int(environ.get("GUILD")))
    if roleCheck(context=context) == False: return
    user = await usernameParser(context=context, username=username, guild=guild)
    if user == None:
            return
    elif message == None:
        await context.channel.send("⚠️ **Error**: You need to send a message to the user")
    elif linkCheck(userID=user.id) == False:
        await userLink(user=user, guild=guild)
        StoredChannelID = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(user.id,)).fetchall()
        channel = client.get_channel(StoredChannelID[0][0])
        finalMessage = f"***Message from the moderators of {guild}:*** \n {message} \n \n ***To respond, simply send a message in this DM***"
        await channel.send(f"`Channel created by {context.author.display_name} via command` \n \n **⚙️ {client.user.display_name}:** {finalMessage}")
        await user.send(finalMessage)
        await context.channel.send(f"✅ Created channel {channel.mention} which is linked to {user.mention}")
    else:
        stored_channel_id = sqliteCursor.execute("SELECT channel_id FROM channels WHERE userID = ?",(user.id,)).fetchall()
        channel = client.get_channel(int(stored_channel_id[0][0]))
        await context.channel.send(f"⚠️ **Error:** This user is already linked to {channel.mention}")
        
        
    

client.run(environ.get("TOKEN"))

import discord
from discord.ext import commands
import asyncio
import secrets
import pyrebase

bot = commands.Bot(command_prefix="!")
firebase = pyrebase.initialize_app(secrets.FIREBASE_CONFIG)
db = firebase.database()

pubg_players = []

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------")

@bot.command(pass_context=True)
async def test(ctx):
    return await bot.say(ctx.message.author)

@bot.command()
async def arg(args):
    return await bot.say("Args: " + args)

@bot.command()
async def firebase(*args):
    if(args[0] == "write"):
        data = {args[2]:args[3]}
        db.child(args[1]).update(data)
        return await bot.say("Someone has just set the child of " + args[1] + " and updated it too " + data)
    elif(args[0] == "remove"):
        return await bot.say("This function is yet to be implemented!")
    elif(args[0] == "read"):
        data = db.child(args[1]).get().val()
        return await bot.say(data)
    else:
        return await bot.say(args[0] + ". Is not a command within the firebase function.")
    data = {args[1]:args[2]}
    db.child(args[0]).update(data)
    return

@bot.command(pass_context=True)
async def pubg(ctx, *args):
    author = ctx.message.author
    if(args[0] == "list"):
        return await bot.say(str(pubg_players))
    elif(args[0] == "join"):
        if(len(pubg_players) >= 4):
            return await bot.say("Sorry but you are not able to join their are all ready 4 people.")
        else:
            if(pubg_players.count(author) > 1):
                return await bot.say("Sorry but " + author + " is already in the team")
            else:
                pubg_players.append(args[1))
                return await bot.say("You are in! Current List: " + str(pubg_players))
        return
    elif(args[0] == "start"):
        if(len(pubg_players) <=4):
            for i in pubg_players:
                if(i <= 4):
                    return await bot.say("You are starting a squad with " + str(pubg_players[i]))
        elif(len(pubg_players) <= 3):
            for i in pubg_players:
                if(i <= 3):
                    return await bot.say("You are starting a trio with " + str(pubg_players[i]))
        elif(len(pubg_players) <= 2):
            for i in pubg_players:
                if(i <= 2):
                    return await bot.say("You are starting a duo with " + str(pubg_players[i]))
        else:
            return await bot.say("There currently isn't a pubg lobby going on! To create one just get 4 or less people to type !pubg join")

@bot.command()
async def stop():
    await bot.say("Stopping Bot...")
    return await exit()

bot.run(secrets.CLIENT_TOKEN)

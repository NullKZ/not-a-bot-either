from configparser import ConfigParser
import discord
import asyncio
#import requests
import json
import sys
import random
#FEATURES
counters = True

#CODE
tokenReader = ConfigParser()
tokenReader.optionxform = str
tokenReader.read('tokens.ini')
tokens = tokenReader['DEFAULT']
active = False
client = discord.Client()
join = lambda x: sum(x,[])
delims = 'd+-'

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    global active
    if message.author == client.user:
        return
    if False: #message.content.lower().startswith("-roll"):
        args = [message.content.lower()[5:].replace(" ","")]
        for delim in delims:
            args = join(f.split(delim) for f in args)
        try:
            numdice = int(args[0])
            dicesize = int(args[1])
            bonus = 0
        except Exception:
            await client.send_message(message.channel, "Invalid input.")
        try:
            bonus = int(args[2])
        except Exception:
            pass
        sign = " +"
        if "-" in message.content.lower()[5:].replace(" ",""):
            sign = " -"
        output = "Rolling "+str(args[0])+"d"+str(args[1])+sign+str(bonus)
        output+=" | `"
        outlist = []
        for i in range(numdice):
            outlist.append(random.randint(1,dicesize))
        if "-" in message.content.lower()[5:].replace(" ",""):
            output+=str(outlist)[1:-1].replace(",","")+" -"+str(bonus)+"`\n"
            output+=str(sum(outlist)-bonus)
        else:
            output+=str(outlist)[1:-1].replace(",","")+" +"+str(bonus)+"`\n"
            output+=str(sum(outlist)+bonus)
        await client.send_message(message.channel, output)
    if message.content.lower().startswith("!bads"):
        if not counters:
            await message.channel.send(content="no u. (Command Disabled.)")
            return
        if active:
            await message.channel.send(content="Already Counting.")
            return
        active=True
        await message.channel.send(content="Counting Bads...")
        fc={}
        dc={}
        sc={}
        tc={}
        num=0
        async for msg in message.channel.history(limit = None):
            num+=1
            if num%100==0:
                print("\r"+str(num), end="")
            if not str(msg.author) in tc:
                tc[str(msg.author)] = 0
            tc[str(msg.author)] += 1
            content = msg.content.lower()
            if "fuck" in content or "fuk" in content or "fuq" in content or "fak" in content:
                if not str(msg.author) in fc:
                    fc[str(msg.author)] = 0
                fc[str(msg.author)] +=1
            if "dam" in content or "damn" in content:
                if not str(msg.author) in dc:
                    dc[str(msg.author)] = 0
                dc[str(msg.author)] +=1
            if "shit" in content:
                if not str(msg.author) in sc:
                    sc[str(msg.author)] = 0
                sc[str(msg.author)] +=1
        baseString = "Fucks Given:\n```"
        for key, value in fc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+= "```Shits Taken:\n```"
        for key, value in sc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+= "```Gods Damned:\n```"
        for key, value in dc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+= "```Messages Sent:\n```"
        for key, value in tc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+="```"
        print(baseString)
        print("Done!")
        active = False
client.run(tokens['discord'])

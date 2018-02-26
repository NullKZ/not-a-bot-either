from configparser import ConfigParser
import discord
import asyncio
import requests
import json
import sys

tokenReader = ConfigParser()
tokenReader.optionxform = str
tokenReader.read('tokens.ini')
tokens = tokenReader['DEFAULT']
active = False
client = discord.Client()

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    global active
    if message.author == client.user:
        return
    if message.content.lower().startswith("!charcount"):
        if active:
            await client.send_message(message.channel, "Already counting. Command ignored.")
            return
        active=True
        edit = await client.send_message(message.channel, "Counting Characters...")
        tc={}
        num=0
        async for msg in client.logs_from(message.channel, limit=400000):
            num+=1
            if num%71==0:
                print("\r"+str(num), end="")
            if not str(msg.author) in tc:
                tc[str(msg.author)] = 0
            tc[str(msg.author)] += len(msg.content)
        baseString = "Messages Sent in Total:\n```"
        for key, value in tc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+="```"
        await client.edit_message(edit, new_content=baseString)
        active=False
        print("")
    if message.content.lower().startswith("!test"):
        if active:
            await client.send_message(message.channel, "Already counting. Command ignored.")
            return
        active=True
        edit = await client.send_message(message.channel, "Counting Bads...")
        fc={}
        sc={}
        tc={}
        num=0
        async for msg in client.logs_from(message.channel, limit=400000):
            num+=1
            if num%71==0:
                print("\r"+str(num), end="")
            if "fuck" in msg.content.lower():
                if not str(msg.author) in fc:
                    fc[str(msg.author)] = 0
                fc[str(msg.author)] +=1
            if "shit" in msg.content.lower():
                if not str(msg.author) in sc:
                    sc[str(msg.author)] = 0
                sc[str(msg.author)] +=1
        baseString = "Fucks Given:\n```"
        for key, value in fc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+= "```Shits Taken:\n```"
        for key, value in sc.items():
            baseString += (key+": "+str(value)+"\n")
        baseString+="```"
        await client.edit_message(edit, new_content=baseString)
        print("")
        active = False
client.run(tokens['discord'])

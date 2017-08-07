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
player = None
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, 'pong!')
    if message.content.startswith('!kill'):
        await client.logout()
    if message.content.startswith('!play'):
        try:
            url = await ytsearch(message.content.split(' ', 1)[1])
            await client.send_message(message.channel, '`Now Playing: '+url[1]+'.`')
            voice = await client.join_voice_channel(message.author.voice.voice_channel)
            global player
            player = await voice.create_ytdl_player(url[0])
            player.start()
        except Exception as e:
            print(e)
    if message.content.startswith('!vol'):
        args = message.content.split(' ', 1)
        if len(args) == 1:
            try:
                await client.send_message(message.channel, '`Volume currently set to '+str(int(player.volume*100))+'.`')
            except Exception as e:
                print(e)
            return
        try:
            val = args[1]
            player.volume = int(val)/100
            await client.send_message(message.channel, '`Volume set to '+str(int(player.volume*100))+'.`')
        except Exception as e:
            print(e)
            await client.send_message(message.channel, '`Invalid volume. Allowed values: 1-200.`')

async def ytsearch(search):
    query = {
        'part':'snippet',
        'q':search,
        'key':tokens['youtube']
    }
    response = requests.get('https://www.googleapis.com/youtube/v3/search', params = query)
    result = json.JSONDecoder().decode(response.text)
    for i in result['items']:
        if i['id']['kind'] == 'youtube#video':
            return 'youtube.com/watch?v='+i['id']['videoId'],i['snippet']['title']

client.run(tokens['discord'])

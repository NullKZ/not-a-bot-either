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

class vc:
    def __init__(self):
        self.voiceCh = None
        self.player = None
        self.vol = 100
        self.active = False

servers = {}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await updateStatus()

@client.event
async def on_server_join(server):
    await updateStatus()
@client.event
async def on_server_join(server):
    await updateStatus()
@client.event
async def on_message(message):
    global servers
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, 'pong!')
    if message.content.startswith('!kill'):
        await client.logout()
    if message.content.startswith('!play'):
        if not message.server.id in servers:
            servers[message.server.id] = vc()
        try:
            url = await ytsearch(message.content.split(' ', 1)[1])
            if servers[message.server.id].voiceCh == None:
                servers[message.server.id].voiceCh = await client.join_voice_channel(message.author.voice.voice_channel)
            if servers[message.server.id].player:
                if not servers[message.server.id].player.is_playing():
                    servers[message.server.id].player = await voiceCh.create_ytdl_player(url[0])
                else:
                    pass #queue it up
            else:
                servers[message.server.id].player = await voiceCh.create_ytdl_player(url[0], after=print('song end'))
            servers[message.server.id].player.start()
            if servers[message.server.id].vol:
                servers[message.server.id].player.volume = vol/100
            await client.send_message(message.channel, '`Now Playing: '+url[1]+'.`')
        except Exception as e:
            print(e.__class__.__name__)
    if message.content.startswith('!dc'):
        try:
            await servers[message.server.id].voiceCh.disconnect()
            servers[message.server.id].voichCh = None
            servers[message.server.id].player = None
        except:
            await client.send_message(message.channel, '`Not Connected to a Voice Channel.`')
    if message.content.startswith('!vol'):
        if not message.server.id in servers:
            servers[message.server.id] = vc()
        args = message.content.split(' ', 1)
        if len(args) == 1:
            await client.send_message(message.channel, '`Volume currently set to '+str(int(servers[message.server.id].vol))+'.`')
            return
        try:
            val = int(args[1])
            if val < 0 or val > 200:
                raise ValueError
            servers[message.server.id].vol = val
            servers[message.server.id].player.volume = val/100
        except Exception as e:
            if e.__class__.__name__ == ValueError.__name__:
                await client.send_message(message.channel, '`Invalid Volume. Volume must be 1-200`')
                return
        await client.send_message(message.channel, '`Volume set to '+str(servers[message.server.id].vol)+'.`')

async def ytsearch(search):
    query = {
        'part':'snippet',
        'q':search,
        'key':tokens['youtube']
    }
    result = json.JSONDecoder().decode(requests.get('https://www.googleapis.com/youtube/v3/search', params = query).text)
    for i in result['items']:
        if i['id']['kind'] == 'youtube#video':
            return 'https://www.youtube.com/watch?v='+i['id']['videoId'],i['snippet']['title']
async def updateStatus():
    status = ' on '+str(len(client.servers))+' server'
    if len(client.servers) > 1:
        status+='s'
    await client.change_presence(game=discord.Game(name=status))


client.run(tokens['discord'])

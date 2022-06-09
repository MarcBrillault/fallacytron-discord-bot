# bot.py
from email.mime import image
import os

import discord
from dotenv import load_dotenv
import requests
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_ROOT = 'http://fallacytron.embryo.fr'
API_PATH = '/api/fallacy'
TMP_IMAGE = 'tmp.png'

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.name)

    guildsString = ', '.join(guilds)
    print(f'{client.user.name} est connecté aux serveurs suivants : {guildsString}')


@client.event
async def on_message(message):
    if f'<@{client.user.id}>' in message.content:
        req = requests.get(API_ROOT + API_PATH)
        if req.status_code != 200:
            return

        api_response = req.json()
        image_response = requests.get(API_ROOT + api_response['image'])
        open(TMP_IMAGE, 'wb').write(image_response.content)

        file = discord.File(TMP_IMAGE)
        await message.channel.send(file=file)

        os.remove(TMP_IMAGE)

client.run(TOKEN)

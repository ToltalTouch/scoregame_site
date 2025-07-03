from replit_run import keep_alive
import logging
import os
import discord

logging.basicConfig(level=logging.INFO, format='%(asctime)s = %(levelname)s: %(message)s')

intents = discord.Intents.default()
intents.message_content = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot conectado: {client.user}')

@client._enable_debug_event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == '!minecraft':
        aviso = 'O servidor do Minebobos está online, abrindo o minecraft de geral...'
        await message.channel.send(aviso)
        logging.info(aviso)

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
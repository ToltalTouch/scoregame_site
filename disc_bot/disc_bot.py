from replit_run import keep_alive
import subprocess
import logging
import os
import discord

logging.basicConfig(level=logging.INFO, format='%(asctime)s = %(levelname)s: %(message)s')

username = os.getlogin()
logging.info(f"{username}")

intents = discord.Intents.default()
intents.message_content = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot conectado: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower() == '!minecraft':
        aviso = 'O servidor do Minebobos está online, abrindo o minecraft de geral...'
        await message.channel.send(aviso)
        logging.info(aviso)
        try:
            subprocess.run([f'C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\TLauncher.exe'])
            logging.info("Minecraft aberto com sucesso.")
            await message.channel.send("Minecraft aberto com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao abrir o Minecraft: {e}")
            await message.channel.send("Houve um erro ao abrir o Minecraft.")


keep_alive()
client.run(os.getenv('DISCORD_KEY'))
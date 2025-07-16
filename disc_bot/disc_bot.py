import threading
import logging
import os
import discord
from flask import Flask, jsonify

# Carrega variáveis de ambiente (funciona tanto local quanto produção)
TOKEN = os.getenv('DISCORD_TOKEN')

# Debug temporário - remover após resolver
logging.info(f"Variáveis de ambiente disponíveis: {list(os.environ.keys())}")
logging.info(f"DISCORD_TOKEN encontrado: {'Sim' if TOKEN else 'Não'}")
if TOKEN:
    logging.info(f"TOKEN (primeiros 10 chars): {TOKEN[:10]}...")
else:
    logging.info("TOKEN é None ou vazio")

app_stage = {'trigger_launch': False}
lock = threading.Lock()
api = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s = %(levelname)s: %(message)s')

@api.route('/check_command', methods=['GET'])
def check_command():
    with lock:
        if app_stage['trigger_launch']:
            logging.info("Sinal de lançamento foi recebido por um cliente")
            return jsonify({'trigger': True, 'status': 'success', 'message': 'Command received.'}), 200
        else:
            logging.info("Nenhum sinal de lançamento pendente")
            return jsonify({'trigger': False, 'status': 'waiting', 'message': 'No command pending'}), 200
    
@api.route('/reset_command', methods=['POST'])
def reset_command():
    with lock:
        app_stage['trigger_launch'] = False
    logging.info("Sinal de lançamento foi resetado por um cliente")
    return jsonify({'status': 'success', 'message': 'Command reset.'}), 200

def run_api():
    api.run(host='0.0.0.0', port=8080)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'bot conectado como {client.user}')
    logging.info('API e BOT estão rodando')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == '!minecraft':
        logging.info("Comando !minecraft recebido. Iniciando o TLauncher...")
        with lock:
            app_stage['trigger_launch'] = True
        await message.channel.send("@here Sinal enviado! O TLauncher será iniciado em breve.")
        
    if message.content.lower() == '!server':
        logging.info("Comando !server recebido. Iniciando o servidor...")
        with lock:
            app_stage['trigger_launch'] = True
        await message.channel.send("@here Sinal enviado! O servidor será iniciado em breve.")

if __name__ == '__main__':
    # Inicia a API em uma thread separada
    api_thread = threading.Thread(target=run_api)
    api_thread.daemon = True
    api_thread.start()
    logging.info("Flask API iniciada na thread secundária")

    # Verifica se o token existe
    if TOKEN is None or TOKEN.strip() == "":
        logging.error("ERRO CRÍTICO: Token do Discord não encontrado.")
        logging.error("Verifique se a variável de ambiente DISCORD_TOKEN está configurada.")
        logging.error("No Render: Settings > Environment > Add Environment Variable")
        # Não encerra o programa, apenas a API Flask continuará rodando
        logging.info("Mantendo apenas a API Flask ativa...")
        import time
        while True:
            time.sleep(60)  # Mantém o processo vivo
    else:
        logging.info("Token encontrado, iniciando Discord Bot...")
        try:
            client.run(TOKEN)
        except Exception as e:
            logging.error(f"Erro ao iniciar o Discord Bot: {e}")
            # Mantém a API ativa mesmo se o bot falhar
            import time
            while True:
                time.sleep(60)
import logging
import requests
import time
import subprocess
import os
import sys
from typing import Optional, Dict, Any
import signal

# Configurações
CONFIG = {
    'SERVER_URL': 'https://scoregame-site.onrender.com',
    'POLL_INTERVAL': 10,
    'REQUEST_TIMEOUT': 10,
    'MAX_RETRIES': 3,
    'RETRY_DELAY': 5,
    'LAUNCH_COOLDOWN': 20
}

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('minecraft_client.log')
    ]
)

class MinecraftLauncher:
    def __init__(self):
        self.running = True
        self.username = os.getlogin()
        self.last_launch_time = 0
        
        # Configurar handler para Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)
        
        logging.info("=== Cliente de Lançamento do Minecraft ===")
        logging.info(f"Servidor: {CONFIG['SERVER_URL']}")
        logging.info(f"Intervalo de polling: {CONFIG['POLL_INTERVAL']}s")
        logging.info(f"Usuário atual: {self.username}")
        logging.info("Para sair, pressione Ctrl+C")

    def _signal_handler(self, signum, frame):
        """Handler para Ctrl+C"""
        logging.info("Recebido sinal de interrupção. Encerrando...")
        self.running = False

    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict[Any, Any]]:
        url = f"{CONFIG['SERVER_URL']}/{endpoint}"
        
        for attempt in range(CONFIG['MAX_RETRIES']):
            try:
                if method == 'GET':
                    response = requests.get(url, timeout=CONFIG['REQUEST_TIMEOUT'])
                elif method == 'POST':
                    response = requests.post(url, json=data, timeout=CONFIG['REQUEST_TIMEOUT'])
                else:
                    raise ValueError(f"Método HTTP não suportado: {method}")
                
                response.raise_for_status()
                
                if response.headers.get('content-type', '').startswith('application/json'):
                    return response.json()
                return {'success': True}
                
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout na tentativa {attempt + 1}/{CONFIG['MAX_RETRIES']}")
            except requests.exceptions.ConnectionError:
                logging.warning(f"Erro de conexão na tentativa {attempt + 1}/{CONFIG['MAX_RETRIES']}")
            except requests.exceptions.HTTPError as e:
                logging.error(f"Erro HTTP {e.response.status_code}: {e}")
                break
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição: {e}")
            except ValueError as e:
                logging.error(f"Erro de validação: {e}")
                break
            
            if attempt < CONFIG['MAX_RETRIES'] - 1:
                logging.info(f"Tentando novamente em {CONFIG['RETRY_DELAY']}s...")
                time.sleep(CONFIG['RETRY_DELAY'])
        
        return None

    def launch_minecraft(self) -> bool:
        """Lança o Minecraft com verificação de cooldown"""
        current_time = time.time()
        
        # Verificar cooldown
        if current_time - self.last_launch_time < CONFIG['LAUNCH_COOLDOWN']:
            remaining = CONFIG['LAUNCH_COOLDOWN'] - (current_time - self.last_launch_time)
            logging.warning(f"Cooldown ativo. Aguarde {remaining:.1f}s antes do próximo lançamento")
            return False
        
        logging.info("Sinal recebido! Tentando iniciar o Minecraft...")
        
        try:
            if os.name == 'nt':  # Windows
                # Lista de métodos para tentar lançar o Minecraft
                launch_methods = [
                    'start minecraft:',  # Protocolo URL do Minecraft
                    'start "" "C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe"',  # Caminho padrão
                    'start "" "C:\\Program Files\\Minecraft Launcher\\MinecraftLauncher.exe"',  # Caminho alternativo
                    'start "" "%APPDATA%\\.minecraft\\MinecraftLauncher.exe"',  # Caminho no AppData
                ]
                
                for i, method in enumerate(launch_methods, 1):
                    try:
                        logging.info(f"Tentativa {i}: {method}")
                        result = subprocess.run(
                            method, 
                            shell=True, 
                            check=True,
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        logging.info(f"Minecraft iniciado com sucesso usando método {i}!")
                        self.last_launch_time = current_time
                        return True
                    except subprocess.CalledProcessError as e:
                        logging.warning(f"Método {i} falhou: {e}")
                        continue
                    except subprocess.TimeoutExpired:
                        logging.info(f"Método {i} executado (timeout esperado)")
                        self.last_launch_time = current_time
                        return True
                
                logging.error("Todos os métodos de lançamento falharam")
                logging.info("Dica: Certifique-se de que o Minecraft Launcher está instalado")
                return False
            else:
                logging.error("Sistema operacional não suportado. Apenas Windows é suportado.")
                return False
                
        except Exception as e:
            logging.error(f"Erro inesperado ao iniciar o Minecraft: {e}")
            return False

    def reset_server_command(self) -> bool:
        logging.info("Resetando sinal de lançamento no servidor...")
        result = self._make_request('reset_command', 'POST')
        
        if result:
            logging.info("Sinal de lançamento resetado com sucesso!")
            return True
        else:
            logging.error("Falha ao resetar o sinal de lançamento")
            return False

    def check_server_command(self) -> bool:
        result = self._make_request('check_command')
        
        if result and isinstance(result, dict):
            trigger = result.get('trigger', False)
            if trigger:
                logging.info("Comando de lançamento detectado!")
                return True
            else:
                logging.debug("Nenhum comando pendente")
                return False
        else:
            logging.warning("Resposta inválida do servidor")
            return False

    def run(self):
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.running:
            try:
                logging.info("Verificando servidor...")
                
                if self.check_server_command():
                    if self.launch_minecraft():
                        self.reset_server_command()
                        logging.info(f"Aguardando {CONFIG['LAUNCH_COOLDOWN']}s antes da próxima verificação...")
                        time.sleep(CONFIG['LAUNCH_COOLDOWN'])
                    else:
                        logging.error("Falha ao lançar o Minecraft")
                
                consecutive_errors = 0  # Reset contador de erros
                
            except Exception as e:
                consecutive_errors += 1
                logging.error(f"Erro no loop principal: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    logging.critical(f"Muitos erros consecutivos ({consecutive_errors}). Encerrando...")
                    break
            
            if self.running:
                logging.info(f"Próxima verificação em {CONFIG['POLL_INTERVAL']}s...")
                time.sleep(CONFIG['POLL_INTERVAL'])
        
        logging.info("Cliente encerrado")

def main():
    try:
        launcher = MinecraftLauncher()
        launcher.run()
    except KeyboardInterrupt:
        logging.info("Interrompido pelo usuário")
    except Exception as e:
        logging.critical(f"Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

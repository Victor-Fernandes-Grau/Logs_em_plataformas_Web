from flask import Flask
from flask_bcrypt import Bcrypt
from loguru import logger
import sys
import os
import threading
import time

# --- Configuração inicial ---
app = Flask(__name__)
app.secret_key = os.getenv('secret_key', 'chave_teste')
bcrypt = Bcrypt(app)

# Garante que a pasta de logs existe
os.makedirs("logs", exist_ok=True)

# Remove handlers padrões
logger.remove()

# Log no terminal (Render)
logger.add(
    sys.stdout,
    format="{time:MMMM D, YYYY - HH:mm:ss} | {level} | {message}"
)

# Log em arquivo (com rotação mensal)
logger.add(
    "logs/app.log",
    rotation="1 month",
    retention="6 months",
    format="{time:MMMM D, YYYY - HH:mm:ss} | {level} | {message}"
)

# --- Rota de teste ---
@app.route('/')
def index():
    logger.info("Usuário acessou a rota principal '/'")
    return "Servidor Flask ativo! Verifique o terminal e o arquivo logs/app.log"


# --- Log automático após inicialização ---
def log_inicio():
    # pequena pausa para garantir que o servidor iniciou
    time.sleep(1)
    logger.info("Servidor Flask iniciado e pronto para receber requisições.")


if __name__ == '__main__':
    logger.info("Iniciando aplicação Flask...")
    threading.Thread(target=log_inicio, daemon=True).start()
    app.run(debug=True)

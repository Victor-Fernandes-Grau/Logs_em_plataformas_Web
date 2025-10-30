from flask import Flask, send_file
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
    format=" LOG_sistema |{time:MMMM D, YYYY - HH:mm:ss} | {level} | {message}"
)

# --- Rota de teste ---
@app.route('/')
def index():
    logger.info("Usuário acessou a rota principal '/'")
    return "Servidor Flask ativo! Verifique o terminal e o arquivo logs/app.log"

@app.route("/logs")
def ver_logs():
    log_path = "logs/app.log"
    if os.path.exists(log_path):
        return send_file(
            log_path,
            mimetype="text/plain",
            as_attachment=True,      # 🔹 força o download automático
            download_name="app.log"  # 🔹 nome do arquivo baixado
        )
    else:
        return "Arquivo de log não encontrado.", 404

# --- Log automático após inicialização ---
def log_inicio():
    time.sleep(1)
    logger.info("Servidor Flask iniciado e pronto para receber requisições.")


if __name__ == '__main__':
    logger.info("Iniciando aplicação Flask...")
    threading.Thread(target=log_inicio, daemon=True).start()
    app.run(debug=True)

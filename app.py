import subprocess
import threading
import time
import os
from flask import Flask, send_file

app = Flask(__name__)

HASHCAT_PATH = 'hashcat'
LOG_FILE = 'hashcat.log'

def run_hashcat():
    command = [HASHCAT_PATH, '-m', '1000', '-O', '-a3', '-i', 'hash.txt']
    with open(LOG_FILE, 'w') as log_file:
        log_file.write("Iniciando Hashcat...\n")
        log_file.write(f"Uso de memória antes: {os.popen('free -m').read()}\n")
        process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)
        process.wait()  # Espera o Hashcat terminar
        log_file.write(f"Uso de memória depois: {os.popen('free -m').read()}\n")
        log_file.write(f"Hashcat terminou com o código de saída {process.returncode}\n")
        if process.returncode != 0:
            log_file.write("\nHashcat terminou com erros.\n")

@app.route('/')
def index():
    return '''
    <h1>Bem-vindo ao Hashcat</h1>
    <p>Você pode <a href="/download_log">baixar o log do Hashcat aqui</a>.</p>
    '''

@app.route('/download_log')
def download_log():
    try:
        with open(LOG_FILE, 'r') as file:
            file_content = file.read()
        return send_file(LOG_FILE, as_attachment=True)
    except FileNotFoundError:
        return "Arquivo de log não encontrado.", 404
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    hashcat_thread = threading.Thread(target=run_hashcat)
    hashcat_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)  # Ajuste a porta se necessário

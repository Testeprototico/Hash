import subprocess
import sys
import os
from flask import Flask, render_template, Response
import time
import threading

app = Flask(__name__)

HASHCAT_PATH = 'hashcat'
LOG_FILE = 'hashcat.log'

def check_and_install_hashcat():
    try:
        # Verifica se o Hashcat está instalado
        subprocess.run([HASHCAT_PATH, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Hashcat está instalado.")
    except subprocess.CalledProcessError:
        print("Hashcat não encontrado. Instalando...")
        install_hashcat()

def install_hashcat():
    # Instala o Hashcat para sistemas baseados em Debian
    if sys.platform.startswith('linux'):
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'hashcat'], check=True)
            print("Hashcat instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar o Hashcat: {e}")
            sys.exit(1)
    else:
        print("Instalação automática do Hashcat não suportada para este sistema operacional.")
        sys.exit(1)

def run_hashcat():
    command = [HASHCAT_PATH, '-m', '1000 -O -a3 -i', 'hash.txt']  # Ajuste os argumentos conforme necessário
    with open(LOG_FILE, 'w') as log_file:
        process = subprocess.Popen(command, stdout=log_file, stderr=log_file, text=True)
        process.wait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    def generate():
        with open(LOG_FILE) as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Espera um pouco antes de tentar ler novamente
                    continue
                yield line
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    check_and_install_hashcat()  # Verifica e instala o Hashcat se necessário
    hashcat_thread = threading.Thread(target=run_hashcat)
    hashcat_thread.start()
    app.run(debug=True, use_reloader=False)

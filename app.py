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

def run_hashcat():
    command = [HASHCAT_PATH, '-m', '1000', '-O', '-a3', '-i', 'hash.txt']
    with open(LOG_FILE, 'w') as log_file:
        print(f"Executando comando: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)
        process.wait()
        print("Hashcat terminou.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log')
def log():
    def generate():
        try:
            with open(LOG_FILE) as f:
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    yield line
        except FileNotFoundError:
            yield "Arquivo de log não encontrado."
        except Exception as e:
            yield f"Erro: {str(e)}"

    return Response(generate(), mimetype='text/plain')


if __name__ == '__main__':
    # check_and_install_hashcat()  # Verificação não necessária no Docker, Hashcat já está instalado
    hashcat_thread = threading.Thread(target=run_hashcat)
    hashcat_thread.start()
    app.run(debug=True, host='0.0.0.0', port=10000)


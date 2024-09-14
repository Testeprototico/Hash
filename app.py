from flask import Flask, render_template, send_file, Response
import subprocess
import threading
import time

app = Flask(__name__)

HASHCAT_PATH = 'hashcat'
LOG_FILE = 'hashcat.log'

def run_hashcat():
    command = [HASHCAT_PATH, '-m', '1000', '-O', '-a3', '-i', 'hash.txt']
    with open(LOG_FILE, 'w') as log_file:
        process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)
        process.wait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_log')
def download_log():
    try:
        return send_file(LOG_FILE, as_attachment=True)
    except FileNotFoundError:
        return "Arquivo de log não encontrado.", 404
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    hashcat_thread = threading.Thread(target=run_hashcat)
    hashcat_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)  # Ajuste a porta se necessário

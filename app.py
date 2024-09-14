from flask import Flask, request, render_template, jsonify
import hashlib
import binascii
import threading
import queue

app = Flask(__name__)

class NTLMCracker(threading.Thread):
    def __init__(self, hash_to_crack, wordlist):
        super().__init__()
        self.hash_to_crack = hash_to_crack
        self.wordlist = wordlist
        self.result = None

    def ntlm_hash(self, password):
        return hashlib.new('md4', password.encode('utf-16le')).digest()

    def run(self):
        q = queue.Queue()
        with open(self.wordlist, 'r') as file:
            for line in file:
                q.put(line.strip())

        while not q.empty():
            password = q.get()
            hashed_password = binascii.hexlify(self.ntlm_hash(password)).decode()
            if hashed_password == self.hash_to_crack:
                self.result = password
                return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack', methods=['POST'])
def crack():
    hash_to_crack = request.form['hash']
    wordlist_file = 'wordlist.txt'
    
    wordlist = request.files['wordlist'].read().decode('utf-8')
    with open(wordlist_file, 'w') as f:
        f.write(wordlist)

    cracker = NTLMCracker(hash_to_crack, wordlist_file)
    cracker.start()
    cracker.join()

    if cracker.result:
        return jsonify({'password': cracker.result})
    else:
        return jsonify({'error': 'Password not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

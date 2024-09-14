from flask import Flask, request, render_template, jsonify
import hashlib
import binascii
import threading
import queue
import os

app = Flask(__name__)

class NTLMCracker(threading.Thread):
    def __init__(self, hash_to_crack, wordlist):
        super().__init__()
        self.hash_to_crack = hash_to_crack
        self.wordlist = wordlist
        self.result = None

    def ntlm_hash(self, password):
        """Generate NTLM hash from a password."""
        return hashlib.new('md4', password.encode('utf-16le')).digest()

    def run(self):
        """Perform the NTLM cracking."""
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
    if 'hash' not in request.form or 'wordlist' not in request.files:
        return jsonify({'error': 'Invalid input'}), 400
    
    hash_to_crack = request.form['hash']
    wordlist_file = 'wordlist.txt'

    # Save uploaded wordlist
    wordlist = request.files['wordlist'].read().decode('utf-8')
    with open(wordlist_file, 'w') as f:
        f.write(wordlist)

    # Start NTLM cracker
    cracker = NTLMCracker(hash_to_crack, wordlist_file)
    cracker.start()
    cracker.join()  # Wait for the thread to finish

    if cracker.result:
        return jsonify({'password': cracker.result})
    else:
        # Keep the endpoint active until a result is found
        return jsonify({'status': 'Searching...'}), 200

if __name__ == '__main__':
    # Use PORT environment variable for port number
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')

def home():
    return "<b>Ele está vivo? ELE ESTÁ VIVO!</b>"

def run():
    app.run(host='127.0.0.1', port=3000) # VERIFICAR HOST E PORTA

def keep_alive():
    t = Thread(target = run)
    t.start()
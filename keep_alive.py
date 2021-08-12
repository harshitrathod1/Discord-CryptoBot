from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return """Hello, Iam Crypto Whale -> ALL IN ONE CRYPTO BOT
    REFER README FOR MORE DETAILS
    """

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
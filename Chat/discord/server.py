from flask import Flask, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Bot Online!"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

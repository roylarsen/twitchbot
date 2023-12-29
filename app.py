from flask import Flask
import requests, tomlkit

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/health")
def get_config():
  with open("/home/rlarsen/.twitch_secrets.toml", "rb") as f:
      data = f.read()

      print(tomlkit.parse(data)["secrets"])
      
  return f'<p>{tomlkit.parse(data)["secrets"]["client_id"]}</p>'

@app.route("/request_token")
def get_token():
  with open("/home/rlarsen/.twitch_secrets.toml") as f:
    creds = f.read()

  data = {

  }

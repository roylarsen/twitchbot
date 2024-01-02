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

  payload = {
    'client_id': tomlkit.parse(creds)["secrets"]["client_id"],
    'client_secret': tomlkit.parse(creds)["secrets"]["client_secret"],
    'grant_type': 'client_credentials'
  }

  r = requests.post('https://id.twitch.tv/oauth2/token', data=payload)

  if "json" in r:
    print(r.json())
    return f"{r.json()['access_token']}"
  else:
    print(r.text)
    return f'{r.text}'

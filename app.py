from quart import Quart, request
from twitchio.ext import commands
import tomlkit, asyncio

app = Quart(__name__)

class Bot(commands.Bot):
  def __init__(self, token):
    super().__init__(token=token, prefix='!', initial_channels=['nuts0x21'])

  async def event_ready(self):
    print(f'Logged in as | {self.nick}')
    print(f'User id is | {self.user_id}')
    print(self.connected_channels)

  async def event_message(self, message):
    if hasattr(message, "echo"):
      print("True")
    if hasattr(message.author, "name"):
      print(f'{message.author.name} == {message.content}')
    await self.handle_commands(message)

  @commands.command()
  async def help(self, ctx: commands.Context):
    #print(dir(ctx))

    msg_content = "Bot Commands:"

    for k in self.commands.keys():
      msg_content += f" // !{k} //"
    
    await ctx.send(msg_content)

  @commands.command()
  async def ping(self, ctx: commands.Context):
    await ctx.send(f'pong!')

@app.route("/")
async def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/health")
async def get_config():
  with open("/home/rlarsen/.twitch_secrets.toml", "rb") as f:
      data = f.read()

      print(tomlkit.parse(data)["secrets"])
      
  return f'<p>{tomlkit.parse(data)["secrets"]["client_id"]}</p>'

@app.route("/auth")
async def auth():
  with open("/home/rlarsen/.twitch_secrets.toml", "rb") as f:
    data = f.read()

  token = tomlkit.parse(data)["secrets"]["client_id"]
  return f'<a href="https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={token}&redirect_uri=http://localhost:5000/&scope=chat%3Aread+chat%3Aedit+whispers%3Aedit">Connect with Twitch</a>'

@app.route("/startup")
async def startup():
  event_loop = asyncio.get_event_loop()

  bot = Bot(token=request.args.get("access_token"))
  event_loop.create_task(bot.start())
  return "started"

@app.route("/testing")
async def testing():
  print(dir(request))
  print(request.view_args)
  return request.args.get("access_token")

app.run()

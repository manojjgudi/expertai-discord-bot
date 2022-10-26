import discord
import os
from expertai.nlapi.cloud.client import ExpertAiClient

discordToken = os.environ['discordToken']
EAI_USERNAME = os.environ["EAI_USERNAME"]
EAI_PASSWORD = os.environ["EAI_PASSWORD"]

expertAiClient = ExpertAiClient()
detector = 'hate-speech'
language = 'en'
intents = discord.Intents(messages=True, guilds=True, message_content=True)
discordClient = discord.Client(intents=intents)


@discordClient.event
async def on_ready():
  print(
    f"Hi there! I am {discordClient.user}, your moderator bot. My job is to make this server a safe place."
  )


@discordClient.event
async def on_message(msg):
  if msg.author != discordClient.user and "Moderator" not in str(
      msg.author.roles):
    content = msg.content
    output = expertAiClient.detection(body={"document": {
      "text": content
    }},
                                      params={
                                        'detector': detector,
                                        'language': language
                                      })
    categories = []
    for category in output.categories:
      categories.append(category.hierarchy[0])
    if len(categories) > 0:
      await msg.delete()
      categoriesString = ",".join(categories)
      await msg.channel.send(
        f"This message posted by {msg.author} was deleted because it contained {categoriesString} content"
      )
      return


try:
  discordClient.run(discordToken)
except:
  os.system("kill 1")

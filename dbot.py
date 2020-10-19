import discord
import re
import os

TOKEN = 'discord token here'
client = discord.Client()

@client.event
async def on_message(message):
    # no self reply
    if message.author == client.user:
        return

    if message.content.startswith("check"):
        msg=message.content
        ips = re.findall(r"[0-9]+(?:\.[0-9]+){3}", msg)
        reply = "Hello {0.author.mention}! Checking the given IP".format(message)
        await message.channel.send(reply)
        command ='python3 start.py '+ips[0]+'>> output.txt'
        os.system(command)
        await message.channel.send(file=discord.File('output.txt'))

@client.event
async def on_ready():
    print("Logged in as: "+client.user.name)
    print("Clent ID is: "+str(client.user.id))
    print("Awaiting commands")

client.run(TOKEN)

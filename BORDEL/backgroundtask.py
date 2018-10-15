import discord
import asyncio

client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='463696422756155413')
    while not client.is_closed:
        counter += 1
        await client.send_message(channel, counter)
        await asyncio.sleep(60) # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run('NDYzNjk0ODI4NzI3ODI4NTEx.Dh0I-Q.PzRrOSBecr9sSeDZdGHVWly5IlA')

import config as c
import os,asyncio,discord
from discord.ext import commands
bot = commands.Bot(commands_prefix="k:", intents=discord.Intents.all())
async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):bot.load_extension(f'cogs.{file[:-3]}')
async def main():
    await load()
    await bot.start(c.token)
asyncio.run(main())

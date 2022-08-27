import config as c
import discord
import asyncio
import os
import discord
from discord.ext import commands
from discord.ext.ui import View, Button, Select


intents=discord.Intents.all()
bot = commands.Bot(command_prefix="<", intents=intents, help_command=None)


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')



async def main():
    await load()
    await bot.start(c.token)



asyncio.run(main())

#return datetime.datetime.now(timezone(loadconfig.__timezone__)).strftime('%H:%M:%S')

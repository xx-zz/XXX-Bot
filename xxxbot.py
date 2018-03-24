import os

import discord
from discord.ext import commands

import xxx
from xxx import core

BOT = core.Bot(command_prefix="", pm_help=None, config_file="config.json")


if __name__ == "__main__":

    BOT.load_config()

    BOT.description = BOT.config.get("description","Description Unavailable!")

    prefix = BOT.config.get("prefix","x ")

    prefixes = [f"{prefix} ", f"{prefix} ".capitalize(), prefix, prefix.capitalize()]

    BOT.command_prefix = commands.when_mentioned_or(*prefixes)

    
    #load all the cogs listed in config file
    for cog in BOT.config["cogs"]:
        extension = f"cogs.{cog}"
        print(extension)
        BOT.load_extension(extension)

    
    BOT.run(BOT.config["discord_token"])
    



import asyncio
import json
import random
import re
import threading

from discord.ext import commands, tasks


def update():
    global config_dict
    threading.Timer(10, update).start()
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)


update()


class hl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.hl.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != self.bot.channel_id or config_dict["commands"]["state"] is False or config_dict["commands"]["hl"] is False:
            return

        for embed in message.embeds:
            try:
                if "I just chose a secret number" in embed.to_dict()["description"]:
                    num = int((re.search("\*\*(.*?)\*\*", embed.to_dict()["description"]).group(1)).title())
                    if num >= 50:
                        await message.components[0].children[0].click()
                    else:
                        await message.components[0].children[2].click()
            except KeyError:
                pass

    @tasks.loop(seconds=42)
    async def hl(self):
        if config_dict["commands"]["hl"] is True and config_dict["commands"]["state"] is True:
            await asyncio.sleep(random.randint(0, 3))
            async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370911072258]):
                await cmd()
                break


async def setup(bot):
    await bot.add_cog(hl(bot))
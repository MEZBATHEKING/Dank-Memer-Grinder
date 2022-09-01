import json
import re
import threading

from discord.ext import commands


def update():
    global config_dict
    threading.Timer(10, update).start()
    with open("config.json", "r") as config_file:
        config_dict = json.load(config_file)


update()


class Autobuy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and message.author.id == 270904126974590976 and config_dict["commands"]["state"] is True:
            for embed in message.embeds:
                print(embed.to_dict())
                # Buy lifesavers
                try:
                    if embed.to_dict()["title"] == "Your lifesaver protected you" and config_dict["autobuy"]["lifesavers"]["state"] is True:
                        remaining = int(re.search("have (.*?) left", embed.to_dict()["description"]).group(1))
                        required = int(config_dict["autobuy"]["lifesavers"]["amount"])
                        if remaining < required:
                            channel = await message.author.create_dm()
                            async for cmd in channel.slash_commands(command_ids=[1011560370864930854]):
                                await cmd(item="Life Saver", quantity=str(required - remaining))
                                break
                            return
                except:
                    pass

                # Confirm purchase
                try:
                    if embed.to_dict()["title"] == "Pending Confirmation" and config_dict["autobuy"]["lifesavers"]["state"] is True:
                        await message.components[0].children[1].click()
                except:
                    pass

        if message.channel.id != self.bot.channel_id or config_dict["commands"]["state"] is False:
            return

        for embed in message.embeds:
            # Shovel
            try:
                if "You don't have a shovel, you need to go buy one." in embed.to_dict()["description"]:
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370948800550]):
                        await cmd(amount="25k")
                        break
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370864930854]):
                        await cmd(item="Shovel", quantity="1")
                        break
                    return
            except KeyError:
                pass

            # Fishing pole
            try:
                if "You don't have a fishing pole, you need to go buy one" in embed.to_dict()["description"]:
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370948800550]):
                        await cmd(amount="25k")
                        break
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370864930854]):
                        await cmd(item="Fishing Pole", quantity="1")
                        break
                    return
            except KeyError:
                pass

            # Hunting rifle
            try:
                if "You don't have a hunting rifle, you need to go buy one." in embed.to_dict()["description"]:
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370948800550]):
                        await cmd(amount="25k")
                        break
                    async for cmd in self.bot.channel.slash_commands(command_ids=[1011560370864930854]):
                        await cmd(item="Hunting Rifle", quantity="1")
                        break
                    return
            except KeyError:
                pass


async def setup(bot):
    await bot.add_cog(Autobuy(bot))
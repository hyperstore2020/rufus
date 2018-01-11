""" admin -- rufus.py """
import os
import config as c

# unused import discord
from discord.ext import commands


class engine:
    """ Different search engines. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def genius(self, *, this):
        """ Search Genius for lyrics
        """
        await self.bot.say ('https://genius.com/search?q=' + this.replace(' ', '%20'))

    @commands.command()
    async def fandom(self, *, this):
        """ Search Fandom for shit
        """
        await self.bot.say ('http://fandom.wikia.com/?s=' + this.replace(' ', '+'))


def setup(bot):
    """ defines setup """
    bot.add_cog(engine(bot))

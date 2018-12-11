""" manager -- rufus.py """
import os
import ctypes
import config as c

from discord.ext import commands


class Manager:
    """ Manager restricted commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """ Stops the bot.
        """
        if ctx.message.author.id in str(c.owner_id):
            await self.bot.say('*Goodbye.*')
            await self.bot.logout()
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def restart(self, ctx):
        """ Restarts the bot. Does not apply file changes.
        """
        if ctx.message.author.id in str(c.owner_id) or str(c.dev_id):
            await self.bot.say('*Restarting bot. Please hold.*')
            await self.bot.logout()
            os.system('python rufus.py')
        else:
            await self.bot.say('*Insufficient privileges*')

    @commands.command(pass_context=True)
    async def img(self, ctx, *, img: str):
        """ Send a local image to a channel.
        """
        if ctx.message.author.id in str(c.owner_id) or str(c.dev_id):
            try:
                if os.path.exists('img/' + img + '.jpg'):
                    await self.bot.send_file(ctx.message.channel, 'img/' + img + '.jpg')
                elif os.path.exists('img/' + img + '.png'):
                    await self.bot.send_file(ctx.message.channel, 'img/' + img + '.png')
            except:
                await self.bot.say('No image named {}.'.format(img))
        else:
            await self.bot.say('*Insufficient privileges*')


def setup(bot):
    """ defines setup """
    bot.add_cog(Manager(bot))

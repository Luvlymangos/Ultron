from discord.ext import commands

from ultron.utils import make_embed
from ultron.core import checks
import discord
import os

class RorqStatus(commands.Cog):
    """This extension handles the time commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.logger = bot.logger

    @commands.command(name='rorqstatus')
    @checks.spam_check()
    @checks.is_whitelist()
    async def _rorq_status(self, ctx):
        """Provides Rorqual status posts.
        '!rorqstatus green Switches rorq status to green.
        '!rorqstatus red Switches rorq status to red."""
        self.logger.info('RorqStatus - {} requested a rorqual status change.'.format(str(ctx.message.author)))
        conversationChannel = ctx.author if ctx.bot.config.dm_only else ctx
        try:
            splittedStr = ctx.message.content.split()
            if len(splittedStr) < 2:
                raise Exception('**ERROR** No status command provided! Do !help rorqstatus for more info')

            status = splittedStr[1].strip().lower()
            rorqStatusChannel = ctx.bot.get_channel(self.config.rorqStatus['channelId'])
            if rorqStatusChannel is None:
                raise Exception('**FATAL ERROR** rorqstatus channel is not properly configured! Please contact system admin')

            if status == 'green':
                current_folder = os.path.dirname(__file__)
                filename = os.path.join(current_folder, 'siege_green.gif')
                file = discord.File(filename)

                await self.delete_messages(rorqStatusChannel)
                await rorqStatusChannel.send("Mine, mine, mine", file=file)
                await conversationChannel.send("Thanks FC. Switched RorqStatus to green!")
            elif status == 'red':
                current_folder = os.path.dirname(__file__)
                filename = os.path.join(current_folder, 'siege_red.jpg')
                file = discord.File(filename)

                await self.delete_messages(rorqStatusChannel)
                await rorqStatusChannel.send("Siege Red girls and boys. No exceptions!", file=file)
                await conversationChannel.send(":( OK OK I'll tell them to dock-up after this cycle")
            else:
                raise Exception('**ERROR:** Unknown status command {} Do !help rorqstatus for more info'.format(status))
        except Exception as e:
            return await conversationChannel.send(str(e))

    def test(self):
        i = 5

    async def delete_messages(self, rorqStatusChannel):
        msgs = []
        async for message in rorqStatusChannel.history(limit=100):
            msgs.append(message)

        await rorqStatusChannel.delete_messages(msgs)
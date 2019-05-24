from discord.ext import commands

from ultron.utils import make_embed
from ultron.core import checks
import discord
import os
import pytz
from datetime import datetime

class RorqStatus(commands.Cog):
    """This extension handles the rorq status change commands."""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.logger = bot.logger

    @commands.command(name='rorqstatus')
    @checks.spam_check()
    @checks.is_rorqstatus_manager()
    async def _rorq_status(self, ctx):
        """Provides Rorqual status posts.
        '!rorqstatus green Switches rorq status to green.
        '!rorqstatus red Switches rorq status to red."""
        self.logger.info('RorqStatus - {} requested a rorqual status change.'.format(str(ctx.message.author)))
        conversationChannel = ctx.author if ctx.bot.config.dm_only else ctx
        try:
            if ctx.channel.id not in self.config.webhook_channel_ids:
                raise Exception("**ERROR** You're not allowed to use this command on this channel!")

            splittedStr = ctx.message.content.split()
            if len(splittedStr) < 2:
                raise Exception('**ERROR** No status command provided! Do !help rorqstatus for more info')

            status = splittedStr[1].strip().lower()
            rorqStatusChannel = ctx.bot.get_channel(self.config.rorqStatus['channelId'])
            if rorqStatusChannel is None:
                raise Exception('**FATAL ERROR** rorqstatus channel is not properly configured! Please contact system admin')

            current_datetime = datetime.now(pytz.timezone('UTC')).strftime('%b %d %Y %H:%M (EVE Time)')
            last_update = "**Last Update** {}".format(current_datetime)
            if status == 'green':
                current_folder = os.path.dirname(__file__)
                filename = os.path.join(current_folder, 'status_green.png')
                file = discord.File(filename)

                await self.delete_messages(rorqStatusChannel)
                await rorqStatusChannel.send("@here {}".format(last_update), file=file)
            elif status == 'red':
                current_folder = os.path.dirname(__file__)
                filename = os.path.join(current_folder, 'status_red.png')
                file = discord.File(filename)

                await self.delete_messages(rorqStatusChannel)
                await rorqStatusChannel.send("@here {}".format(last_update), file=file)
            else:
                raise Exception('**ERROR:** Unknown status command {} Do !help rorqstatus for more info'.format(status))
        except Exception as e:
            return await conversationChannel.send(str(e))

    async def delete_messages(self, rorqStatusChannel):
        msgs = []
        async for message in rorqStatusChannel.history(limit=100):
            msgs.append(message)

        await rorqStatusChannel.delete_messages(msgs)
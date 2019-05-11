from discord.ext import commands

from ultron.utils import make_embed
from ultron.core import checks
import discord
import os
import pytz
import re
from datetime import datetime

class FCPing(commands.Cog):
    """This extension handles the fleet ping commands."""

    pattern = re.compile("(.*)\\s+(.*)\\s+(.*)");

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.logger = bot.logger

    @commands.command(name='fcping')
    @checks.spam_check()
    @checks.is_whitelist()
    async def _fc_ping(self, ctx):
        """Provides Fleet ping posts.
        '!fcping channel_id message sends the message to associated channel"""
        self.logger.info('FCPing - {} requested a fleet ping change.'.format(str(ctx.message.author)))
        conversationChannel = ctx.author if ctx.bot.config.dm_only else ctx
        try:
            if ctx.channel.id not in self.config.webhook_channel_ids:
                raise Exception("**ERROR** You're not allowed to use this command on this channel!")
            splittedStr = ctx.message.content.split(' ', 2)
            if len(splittedStr) < 3:
                raise Exception('**ERROR** Invalid command! Do !help fcping for more info')

            channelIdToPing = int(splittedStr[1]);

            if channelIdToPing not in self.config.fcPings['allowedChannelIds']:
                raise Exception("**ERROR** You're not allowed to ping this channel. Please contact system admin")

            channelToPing = ctx.bot.get_channel(channelIdToPing)
            if channelToPing is None:
                raise Exception('**FATAL ERROR** Requested ping channel does not exist, looks like a configuration issue. Please contact system admin')

            message = splittedStr[2];

            current_datetime = datetime.now(pytz.timezone('UTC')).strftime('%b %d %Y %H:%M (EVE Time)')
            timestamp = "Timestamp: {}".format(current_datetime)
            await channelToPing.send("{}\n{}".format(timestamp, message))

        except Exception as e:
            return await conversationChannel.send(str(e))


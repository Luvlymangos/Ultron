from .fc_ping import FCPing


def setup(bot):
    bot.add_cog(FCPing(bot))

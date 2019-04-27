from .rorq_status import RorqStatus


def setup(bot):
    bot.add_cog(RorqStatus(bot))

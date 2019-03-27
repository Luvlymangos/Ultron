"""Ultron - An EVE Online Discord Bot"""

import argparse
import asyncio
import sys

import discord
from ultron.core import bot, events
from ultron.utils import logger
from ultron.utils import ExitCodes

if discord.version_info.major < 1:
    print("You are not running discord.py v1.0.0a or above.\n\n"
          "Ultron requires the new discord.py library to function "
          "correctly. Please install the correct version.")
    sys.exit(1)


def run_ultron(debug=None, launcher=None):
    ultron = bot.ultron()
    events.init_events(ultron, launcher=launcher)
    ultron.logger = logger.init_logger(debug_flag=debug)
    ultron.load_extension('ultron.core.commands')
    ultron.load_extension('ultron.core.extension_manager')
    for ext in ultron.preload_ext:
        ext_name = ("ultron.extensions." + ext)
        ultron.load_extension(ext_name)
    loop = asyncio.get_event_loop()
    if ultron.token is None or not ultron.default_prefix:
        ultron.logger.critical("Token and prefix must be set in order to login.")
        sys.exit(1)
    try:
        loop.run_until_complete(ultron.start(ultron.token))
    except discord.LoginFailure:
        ultron.logger.critical("Invalid token")
        loop.run_until_complete(ultron.logout())
        ultron._shutdown_mode = ExitCodes.SHUTDOWN
    except KeyboardInterrupt:
        ultron.logger.info("Keyboard interrupt detected. Quitting...")
        loop.run_until_complete(ultron.logout())
        ultron._shutdown_mode = ExitCodes.SHUTDOWN
    except Exception as e:
        ultron.logger.critical("Fatal exception", exc_info=e)
        loop.run_until_complete(ultron.logout())
    finally:
        code = ultron._shutdown_mode
        sys.exit(code.value)


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="ultron - An EVE Online Discord Bot")
    parser.add_argument(
        "--debug", "-d", help="Enabled debug mode.", action="store_true")
    parser.add_argument(
        "--launcher", "-l", help=argparse.SUPPRESS, action="store_true")
    return parser.parse_args()


def main():
    args = parse_cli_args()
    run_ultron(debug=args.debug, launcher=args.launcher)


if __name__ == '__main__':
    main()

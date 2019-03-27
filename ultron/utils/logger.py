import logging
import logging.handlers
import sys
import os


def init_logger(debug_flag=False):
    log_level = logging.INFO if debug_flag else logging.WARNING

    # d_py logs
    discord_log = logging.getLogger("discord")
    discord_log.setLevel(log_level)
    console = logging.StreamHandler()
    console.setLevel(log_level)
    discord_log.addHandler(console)

    # ultron logs
    logger = logging.getLogger("ultron")

    ultron_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M:%S]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ultron_format)
    logger.setLevel(log_level)

    if os.getenv("LOG") is not None:
        logfile_path = os.getenv("LOG")
    else:
        logfile_path = os.getcwd() + '/ultron/logs/ultron.log'

    fhandler = logging.handlers.RotatingFileHandler(
        filename=str(logfile_path), encoding='utf-8', mode='a',
        maxBytes=400000, backupCount=20)
    fhandler.setFormatter(ultron_format)

    logger.addHandler(fhandler)
    if debug_flag:
        logger.addHandler(stdout_handler)

    return logger

# -*- coding: utf-8 -*-

import logging
from logging.handlers import SysLogHandler


def get_logger(server_name, log_format, log_level):
    log_format = logging.Formatter(log_format)

    # sys log
    sys_log = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_LOCAL3)
    sys_log.setFormatter(log_format)

    # console log
    console_log = logging.StreamHandler()
    console_log.setFormatter(log_format)

    # run_log
    logger = logging.getLogger(server_name)
    logger.handlers = []

    # logger.addHandler(sys_log)
    logger.addHandler(console_log)
    logger.setLevel(log_level)

    return logger


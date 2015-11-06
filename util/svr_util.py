# -*- coding: utf-8 -*-

import logging
from logging.handlers import SysLogHandler, TimedRotatingFileHandler


def get_console_handler(log_format, log_level):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(log_level)
    return handler


def get_syslog_handler(log_format, log_level):
    handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_LOCAL3)
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(log_level)
    return handler


def get_file_handler(file_name, log_format, log_level):
    handler = TimedRotatingFileHandler(file_name, 'D')
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(log_level)
    return handler


def get_logger(server_name, svr_conf):
    logger = logging.getLogger(server_name)
    logger.handlers = []

    if svr_conf['log.console']:
        handler = get_console_handler(svr_conf['log.console.format'], svr_conf['log.console.level'])
        logger.addHandler(handler)

    if svr_conf['log.syslog']:
        handler = get_syslog_handler(svr_conf['log.syslog.format'], svr_conf['log.syslog.level'])
        logger.addHandler(handler)

    file_name = svr_conf['log.file_log']
    if file_name:
        handler = get_file_handler(file_name, svr_conf['log.file_log.format'], svr_conf['log.file_log.level'])
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)

    return logger



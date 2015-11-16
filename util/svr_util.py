# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import SysLogHandler, TimedRotatingFileHandler, SMTPHandler


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


def get_email_handle(log_format, log_level, mail_config, subject):
    handler = SMTPHandler(mail_config['host'], mail_config['from'][0],
                          mail_config['target'], subject, mail_config['from'])
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(log_format))
    return handler


def get_logger(server_name, svr_conf):
    logger = logging.getLogger(server_name)

    logger.handlers = []
    logger.setLevel(logging.INFO)

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

    if svr_conf['log.email']:
        handler = get_email_handle(svr_conf['log.email.format'], svr_conf['log.email.level'],
                                   svr_conf['log.email.config'], 'Email_Log: %s' % svr_conf['svr.name'])
        logger.addHandler(handler)

    return logger


def out_put_pid_file():
    with open('svr.pid', 'w') as f:
        f.write(str(os.getpid()))

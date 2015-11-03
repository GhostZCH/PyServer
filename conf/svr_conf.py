# -*- coding: utf-8 -*-

CONFIG_DICT = {
    # server
    'svr.name': 'my_server',
    'svr.timer.min_span': 1,
    'svr.close.force_close_delay': 10,
    'svr.close.wait_lock_delay': 1,

    # log
    'log.level': 'INFO',
    'log.format': '< %(levelname)s: %(name)s(%(process)d) > [%(filename)s: %(lineno)d] >> %(message)s ',

    # other
    'other.x': 5
}

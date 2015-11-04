# -*- coding: utf-8 -*-

import os
import time
import signal
import threading
import traceback

from util import svr_util
from conf import svr_conf
from svr_timer import TimerObserver, PeriodTimer, FixedPeriodTimer

force_exit = os._exit


class ServerBase(object):
    def __init__(self):
        self._is_run = None
        self._is_close = False
        self._is_start = False
        self._run_lock = threading.RLock()
        self._timer_observer = TimerObserver()
        signal.signal(signal.SIGINT, self._event_signal)
        signal.signal(signal.SIGUSR1, self._event_signal)

    def _reload(self):
        reload(svr_conf)
        self.conf = svr_conf.CONFIG_DICT
        self.name = self.conf['svr.name']

        self.logger = svr_util.get_logger(svr_conf.CONFIG_DICT['svr.name'], svr_conf.CONFIG_DICT['log.format'], svr_conf.CONFIG_DICT['log.level'])
        self.warn = self.logger.warn
        self.info = self.logger.info
        self.err = self.logger.error

        self.on_reload()

    def _event_signal(self, sig, farm):
        self.warn('signal %s' % sig)
        if sig == signal.SIGINT:
            self.close()
        elif sig == signal.SIGUSR1:
            self._reload()
        else:
            force_exit(-1)

    def close(self, delay=None, exit_code=0):
        if self._is_close:
            return
        self._is_close = True

        if not delay:
            delay = self.conf['svr.close.force_close_delay']
        self.err('close: delay = %s, exit_code = %s' % (delay, exit_code))

        threading.Timer(interval=delay, function=force_exit, args=[exit_code]).start()

        self._is_run = False

        wait_time = 0
        min_span = 0.1
        while wait_time < int(self.conf['svr.close.wait_lock_delay']):
            if self._run_lock.acquire(0):
                self.info('self._run_lock.acquire')
                break
            time.sleep(min_span)
            wait_time += min_span

        try:
            self.on_close()
        except:
            self.err(traceback.format_exc())

        force_exit(exit_code)

    def start(self):
        if self._is_start:
            self.warn('program has already start!')
        self._is_start = True

        try:
            self._reload()
            self.on_start()
            self.run()
        except Exception as ex:
            self.on_except(ex, traceback.format_exc())

    def forever(self):
        if self._is_start:
            self.warn('program has already start!')
        self._is_start = True

        try:
            self._reload()
            self.on_start()
        except Exception as ex:
            self.on_except(ex, traceback.format_exc())

        self._is_run = True
        while self._is_run:
            with self._run_lock:
                try:
                    self.run()
                except Exception as ex:
                    self.on_except(ex, traceback.format_exc())

    # ------------- abstract function --------------
    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_start(self):
        pass

    def on_except(self, ex, trace_back):
        pass

    def run(self):
        pass

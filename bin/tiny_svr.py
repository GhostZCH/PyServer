# -*- coding: utf-8 -*-

import os
import time
import signal
import threading
import traceback

from util import svr_util
from conf import svr_conf

from tiny_timer import (TinyTimerObserver,
                        TinyThreadTimerObserver,
                        PeriodTimer,
                        FixedPeriodTimer)


class TinyServer:
    def __init__(self):
        self._is_run = False
        self._is_close = False
        self._is_reload = False
        self._is_closing = False

        self._logger = None
        self._handler = None

        self._timer = None
        self._thread_timer = None
        self._last_report_time = None

        self._conf = svr_conf.CONF
        self._context = {}

        signal.signal(signal.SIGINT, self._signal)
        signal.signal(signal.SIGTERM, self._signal)
        signal.signal(signal.SIGUSR1, self._signal)

        svr_util.out_put_pid_file(self.get_name())

    def get_handler(self):
        raise NotImplementedError

    def get_name(self):
        return self._conf['svr.name']

    def on_reload(self):
        pass

    def on_start(self):
        pass

    # ------------- public function --------------
    def close(self, delay=None, exit_code=0):
        if self._is_closing:
            return

        self._is_closing = True
        if not delay:
            delay = self._conf['svr.close.force_close_delay']

        self.error('close: delay = %s, exit_code = %s' % (delay, exit_code))

        threading.Timer(interval=delay, function=svr_util.force_exit, args=[exit_code]).start()

        try:
            self._close()
        except:
            self.error(traceback.format_exc())

        svr_util.force_exit(exit_code)

    def forever(self):
        if self._is_run:
            return

        self._is_run = True
        self._start()
        while self._is_run:
            try:
                if self._is_close:
                    self.close()
                    return

                if self._is_reload:
                    self._reload()
                    continue

                self._timer.run()
                self._handler.run()
                self.running_report()

            except Exception as ex:
                if not self._on_error(ex, traceback.format_exc()):
                    return

    def running_report(self):
        self._last_report_time = time.time()

    def add_timer(self, key, timer, is_thread_timer=False):
        if is_thread_timer:
            return self._thread_timer.add(key, timer)
        else:
            return self._timer.add(key, timer)

    def remove_timer(self, key, is_thread_timer=False):
        if is_thread_timer:
            return self._thread_timer.remove(key)
        else:
            return self._timer.remove(key)

    def _on_error(self, ex, trace):
        try:
            if self._handler.on_except(ex, trace):
                return True
            else:
                self._handler.close()
                return False
        except:
            self.error(traceback.format_exc())
            return False

    def _reload(self):
        self.warn("reloading ...")
        self._clear_timer()
        self._output_summary()
        self._handler.close()

        reload(svr_util)
        reload(svr_conf)
        self.on_reload()

        self._start()

        self._is_reload = False

    def _close(self):
        self.warn("close ...")
        self._clear_timer()
        self._output_summary()

        self._is_run = False
        self._handler.close()

    def _start(self):
        self._conf = svr_conf.CONF
        self._get_logger()
        self._handler = self.get_handler()
        self._handler.start()
        self._init_timer()
        self.on_start()

    def _signal(self, sig, _):
        self.warn('signal %s' % sig)

        if sig in (signal.SIGINT, signal.SIGTERM):
            self._is_close = True
        elif sig == signal.SIGUSR1:
            self._is_reload = True

    def _get_logger(self):
        self._logger = svr_util.get_logger(self.get_name(), self._conf)

        self.info = self._logger.info
        self.warn = self._logger.warn
        self.error = self._logger.error

    def _states_check(self):
        if not self._last_report_time:
            return

        report_time = self._conf['svr.timer.run_status_check_time_span']
        delta_time = time.time() - self._last_report_time
        if delta_time < report_time:
            return

        self.error('run_states_check: not receive report in %s s, start auto-exit!' % report_time)

        # close safely
        os.kill(os.getpid(), signal.SIGINT)

        # if can't close safely force_exit
        delay = self._conf['svr.close.force_close_delay']
        threading.Timer(interval=delay, function=svr_util.force_exit, args=[-3]).start()

    def _output_summary(self):
        self.warn('<SUMMARY> %s' % self._handler.get_summary())

    def _clear_timer(self):
        self._timer.clear()
        self._thread_timer.clear()

    def _init_timer(self):
        self._timer = TinyTimerObserver(self._logger)
        self._thread_timer = TinyThreadTimerObserver(self._logger, self._conf['svr.timer.min_span'])

        check_timer = PeriodTimer(self._states_check, self._conf['svr.timer.run_status_check_time_span'])
        summary_timer = FixedPeriodTimer(self._output_summary, self._conf['svr.timer.summary_output_time_point'])

        self._thread_timer.add('check_timer', check_timer)
        self._thread_timer.add('summary_timer', summary_timer)
        self._thread_timer.start()

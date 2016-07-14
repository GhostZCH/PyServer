# -*- coding: utf-8 -*-

import os
import time
import signal
import threading
import traceback

from util import svr_util
from conf import svr_conf

from tiny_timer import TimerObserver, PeriodTimer, FixedPeriodTimer


class TinyServer:
    def __init__(self, handler_class, argv):
        self._is_run = False
        self._is_close = False
        self._is_reload = False

        self._timer_observer = None
        self._last_report_time = None

        self._handler = None

        self._argv = argv
        self._handler_class = handler_class

        signal.signal(signal.SIGINT, self._event_signal)
        signal.signal(signal.SIGTERM, self._event_signal)
        signal.signal(signal.SIGUSR1, self._event_signal)

        svr_util.out_put_pid_file()

    def _reload(self):
        self.warn("reload ...")
        reload(svr_util)
        reload(svr_conf)

    def _event_signal(self, sig, frame):
        self.warn('signal %s' % sig)

        if sig in (signal.SIGINT, signal.SIGTERM):
            self._is_close = True
        elif sig == signal.SIGUSR1:
            self._is_reload = True

    def _event_run_states_check(self):
        if not self._last_report_time:
            return

        report_time = self.conf['svr.timer.run_status_check_time_span']
        delta_time = time.time() - self._last_report_time
        if delta_time < report_time:
            return

        self.error('run_states_check: not receive report in %s s, start auto-exit!' % report_time)
        self.close(exit_code=-3)

    def _event_output_summary(self):
        self.warn('<SUMMARY> %s' % self._handler.get_summary())

    def _reset_sys_timer(self):
        if self._timer_observer:
            self._timer_observer.stop()
            self._timer_observer.clear_timer()

        check_timer = PeriodTimer(self._event_run_states_check, self.conf['svr.timer.run_status_check_time_span'])
        summary_timer = FixedPeriodTimer(self._event_output_summary, self.conf['svr.timer.summary_output_time_point'])

        self._timer_observer = TimerObserver(int(self.conf['svr.timer.min_span']), self.on_except, self.logger)

        self._timer_observer.add_timer('check_timer', check_timer)
        self._timer_observer.add_timer('summary_timer', summary_timer)

    # ------------- public function --------------
    def close(self, delay=None, exit_code=0):
        if self._is_close:
            return
        self._is_close = True

        if not delay:
            delay = self.conf['svr.close.force_close_delay']

        self.err('close: delay = %s, exit_code = %s' % (delay, exit_code))
        self.warn('<SUMMARY> %s' % str(self.get_summary()))

        threading.Timer(interval=delay, function=svr_util.force_exit, args=[exit_code]).start()

        self._is_run = False

        try:
            self.on_close()
        except:
            self.error(traceback.format_exc())

        svr_util.force_exit(exit_code)

    def forever(self):
        if not self._per_start():
            return

        try:
            self.on_start()
        except Exception as ex:
            trace = traceback.format_exc()
            try:
                self.on_except(ex, traceback.format_exc())
            except:
                print trace
            return

        self._is_run = True
        while self._is_run:
            with self._run_lock:
                try:
                    self.run()
                except Exception as ex:
                    self._on_exception(ex, traceback.format_exc())

    def running_report(self):
        self._last_report_time = time.time()

    def add_timer(self, key, timer):
        return self._timer_observer.add_timer(key, timer)

    def remove_timer(self, key):
        return self._timer_observer.remove_timer(key)

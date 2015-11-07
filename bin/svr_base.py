# -*- coding: utf-8 -*-

import os
import time
import signal
import threading
import traceback

from util import svr_util
from conf import svr_conf
from svr_timer import TimerObserver, PeriodTimer, FixedPeriodTimer

_force_exit = os._exit


class ServerBase(object):
    def __init__(self):
        self._is_run = False
        self._is_close = False
        self._is_start = False

        self._timer_observer = None
        self._last_report_time = None
        self._run_lock = threading.RLock()

        signal.signal(signal.SIGINT, self._event_signal)
        signal.signal(signal.SIGTERM, self._event_signal)
        signal.signal(signal.SIGUSR1, self._event_signal)

        svr_util.out_put_pid_file()

    def _reload(self):
        reload(svr_conf)
        self.conf = svr_conf.CONFIG_DICT
        self.name = self.conf['svr.name']

        self.logger = svr_util.get_logger(self.name, self.conf)
        self.warn = self.logger.warn
        self.info = self.logger.info
        self.err = self.logger.error

        if self.conf['svr.log_conf_on_reload']:
            self.warn(self.conf)

        self._reset_sys_timer()
        self.on_reload()

        time.sleep(self.conf['svr.timer.min_span'])
        self._timer_observer.start()

    def _event_signal(self, sig, frame):
        self.warn('signal %s' % sig)

        if sig in (signal.SIGINT, signal.SIGTERM):
            self.close()
        elif sig == signal.SIGUSR1:
            self._reload()
        else:
            _force_exit(-1)

    def _event_run_states_check(self):
        if not self._last_report_time:
            return

        report_time = self.conf['svr.timer.run_status_check_time_span']
        delta_time = time.time() - self._last_report_time
        if delta_time < report_time:
            return

        self.err('run_states_check: not receive report in %s s, start auto-exit!' % report_time)
        self.close(exit_code=-3)

    def _event_output_summary(self):
        self.warn('<SUMMARY> %s' % str(self.get_summary()))

    def _reset_sys_timer(self):
        if self._timer_observer:
            self._timer_observer.clear_timer()
            self._timer_observer.stop()

        check_timer = PeriodTimer(self._event_run_states_check, self.conf['svr.timer.run_status_check_time_span'])
        summary_timer = FixedPeriodTimer(self._event_output_summary, self.conf['svr.timer.summary_output_time_point'])

        self._timer_observer = TimerObserver(int(self.conf['svr.timer.min_span']), self.on_except, self.logger)
        self._timer_observer.add_timer('check_timer', check_timer)
        self._timer_observer.add_timer('summary_timer', summary_timer)

    def _per_start(self):
        if self._is_start:
            self.warn('program has already start!')
            return False

        self._is_start = True
        return True

    # ------------- public function --------------
    def close(self, delay=None, exit_code=0):
        if self._is_close:
            return
        self._is_close = True

        if not delay:
            delay = self.conf['svr.close.force_close_delay']

        self.err('close: delay = %s, exit_code = %s' % (delay, exit_code))
        self.warn('<SUMMARY> %s' % str(self.get_summary()))

        threading.Timer(interval=delay, function=_force_exit, args=[exit_code]).start()

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

        _force_exit(exit_code)

    def start(self):
        if not self._per_start():
            return

        try:
            self._reload()
            self.on_start()
            self.run()
        except Exception as ex:
            self.on_except(ex, traceback.format_exc())

    def forever(self):
        if not self._per_start():
            return

        try:
            self._reload()
            self.on_start()
        except Exception as ex:
            trace = traceback.format_exc()
            try:
                self.on_except(ex, traceback.format_exc())
            except:
                print trace

        self._is_run = True
        while self._is_run:
            with self._run_lock:
                try:
                    self.run()
                except Exception as ex:
                    self.on_except(ex, traceback.format_exc())

    def running_report(self):
        self._last_report_time = time.time()

    def add_timer(self, key, timer):
        return self._timer_observer.add_timer(key, timer)

    def remove_timer(self, key):
        return self._timer_observer.remove_timer(key)

    # ------------- abstract function --------------
    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_start(self):
        pass

    def on_except(self, ex, trace_back):
        pass

    def get_summary(self):
        pass

    def run(self):
        pass

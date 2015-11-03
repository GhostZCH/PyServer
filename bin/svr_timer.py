# -*- coding: utf-8 -*-
import time
import datetime
from threading import Event
from threading import Thread


class _AbstractTimer(object):
    def run(self, time_stamp):
        """
        返回值 True 表示执行成功，返回 False
        """
        return False


class PeriodTimer(_AbstractTimer):
    def __init__(self, target, interval, max_run_count=None):
        self._run_count = 0
        self._target = target
        self._interval = interval
        self._max_run_count = max_run_count
        self._next_time = time.time() + interval

    def run(self, time_stamp):
        """
        返回值 True 表示执行成功，返回 False
        """
        if time_stamp < self._next_time:
            return True

        self._next_time = time.time() + self._interval
        self._target()

        if self._max_run_count:
            return self._max_run_count > self._run_count
        return True

class FixedPeriodTimer(PeriodTimer):
    """
    设置固定时间的周期性定时器 D H
    """
    _TYPE_DICT = {
        'D': (24 * 3600, datetime.timedelta(days=1)),
        'H': (3600, datetime.timedelta(hours=1))
    }

    def __init__(self, target, fix_type, max_run_count=None):
        if fix_type not in FixedPeriodTimer._TYPE_DICT:
            raise Exception('unknown FixedPeriodTimer type, should be "D"(per day) or "H"(per hour)')
        PeriodTimer.__init__(self, target, FixedPeriodTimer._TYPE_DICT[fix_type][0], max_run_count)
        next_time = datetime.datetime.now() + FixedPeriodTimer._TYPE_DICT[fix_type][1]
        self._next_time = next_time.ctime()

    @classmethod
    def _get_start_time(cls, fix_type):

        return 0


class TimerObserver(Thread):
    def __init__(self, interval, on_except=None):
        """
        :param interval: 时间间隔
        :param target: 执行的函数
        :param args: 传递给 target 的参数（元组）
        :param kwargs:  传递给 target 的参数（字典）
        :param max_times: 执行的最大次数[1, 2, 3 ...]，None 表示不限制次数，直到 stop()
        """

        Thread.__init__(self)
        self._interval = interval
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._finish_event = Event()
        self._max_times = max_times
        self._event_on_except = on_except

    def run(self):
        while True:
            self._finish_event.wait(timeout=self._interval)

            if self._finish_event.is_set():
                return
            try:
                self._target(*self._args, **self._kwargs)
            except BaseException, ex:
                if self._event_on_except(ex):
                    raise

            if self._max_times:
                self._max_times -= 1
                if self._max_times <= 0:
                    if self._event_on_finish:
                        self._event_on_finish
                    return

    def stop(self):
        self._finish_event.set()
        self._event_on_finish()

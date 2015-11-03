# -*- coding: utf-8 -*-

import time
import datetime
import traceback

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
        'D': (24 * 3600, datetime.timedelta(days=1), '%Y%m%d'),
        'H': (3600, datetime.timedelta(hours=1), '%Y%m%d%H')
    }

    def __init__(self, target, fix_type, max_run_count=None):
        if fix_type not in FixedPeriodTimer._TYPE_DICT:
            raise Exception('unknown FixedPeriodTimer type, should be "D"(per day) or "H"(per hour)')
        PeriodTimer.__init__(self, target, FixedPeriodTimer._TYPE_DICT[fix_type][0], max_run_count)

        self._next_time = FixedPeriodTimer._get_start_time(fix_type)

    @classmethod
    def _get_start_time(cls, fix_type):
        next_time = datetime.datetime.now() + FixedPeriodTimer._TYPE_DICT[fix_type][1]
        next_time = next_time.strftime(FixedPeriodTimer._TYPE_DICT[fix_type][2])
        next_time = datetime.datetime.strptime(next_time, FixedPeriodTimer._TYPE_DICT[fix_type][2])
        return time.mktime(next_time.timetuple())


class TimerObserver(Thread):
    def __init__(self, min_interval, on_except):
        """
        :param interval: 时间间隔
        :param target: 执行的函数
        :param args: 传递给 target 的参数（元组）
        :param kwargs:  传递给 target 的参数（字典）
        :param max_times: 执行的最大次数[1, 2, 3 ...]，None 表示不限制次数，直到 stop()
        """

        Thread.__init__(self)
        self._interval = min_interval
        self._timer_dict = {}
        self._finish_event = Event()
        self._event_on_except = on_except

    def add_timer(self, key, timer):
        if key in self._timer_dict:
            return False

        self._timer_dict[key] = timer

    def remove_timer(self, key):
        if key not in self._timer_dict:
            return False

        self._timer_dict.pop(key)
        return True

    def run(self):
        while True:
            self._finish_event.wait(timeout=self._interval)

            if self._finish_event.is_set():
                return

            time_stamp = time.time()
            for timer in self._timer_dict.values():
                try:
                    timer.run(time_stamp)
                except Exception as ex:
                    self._event_on_except(ex, traceback.format_exc())

    def stop(self):
        self._finish_event.set()
        self._event_on_finish()

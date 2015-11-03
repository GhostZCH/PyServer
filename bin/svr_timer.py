# -*- coding: utf-8 -*-

from threading import Event
from threading import Thread


class Timer(Thread):
    def __init__(self, interval, target, max_times=None, args=[], kwargs={}, on_except=None, on_finish=None):
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
        self._event_on_finish = on_finish

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

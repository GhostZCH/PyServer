import os
import signal
import threading

from util import svr_util
from conf import svr_conf

force_exit = os._exit


class ServerBase(object):
    def __init__(self):
        self._reload()
        signal.signal(signal.SIGINT, self._event_signal)
        signal.signal(signal.SIGTERM, self._event_signal)

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
            self._reload()
        elif signal == signal.SIGTERM:
            self.close()
        else:
            force_exit(-1)

    def close(self, delay=None, exit_code=0):
        if not delay:
            delay = self.conf['svr.force_close_delay']
        threading.Timer(interval=delay, function=force_exit, args=[exit_code]).start()
        self.on_close()

    def start(self):
        try:
            self.on_start()
            self.run()
        except Exception as ex:
            self.on_except(ex)

    def forever(self):
        try:
            self.on_start()
        except Exception as ex:
            self.on_except(ex)

        while True:
            try:
                self.run()
            except Exception as ex:
                self.on_except(ex)

    # ------------- abstract function --------------
    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_start(self):
        pass

    def on_except(self, ex):
        pass

    def run(self):
        pass

import os
import signal
import threading

import server_util
import conf

force_exit = os._exit


class ServerBase(object):
    def __init__(self):
        self._reload()
        signal.signal(signal.SIGINT, self._event_signal)
        signal.signal(signal.SIGTERM, self._event_signal)

    def _reload(self):
        reload(conf)
        self.conf = conf.Config
        self.name = self.conf['svr.name']

        self.logger = server_util.get_logger(conf.Config['svr.name'], conf.Config['log.format'], conf.Config['log.level'])
        self.warn = self.logger.warn
        self.info = self.logger.info
        self.err = self.logger.error

        self.on_reload()

    def _event_signal(self, sig, farm):
        self.warn('signal %s' % sig)
        if sig == signal.SIGINT:
            self._reload()
        elif signal == signal.SIGTERM:
            self._close()
        else:
            force_exit(-1)

    def _close(self):
        threading.Timer(self.conf['svr.force_close_delay'], force_exit).start()
        self.on_close()

    def start(self):
        self.on_start()
        self.run()

    # ------------- abstract function --------------
    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_start(self):
        pass

    def run(self):
        pass

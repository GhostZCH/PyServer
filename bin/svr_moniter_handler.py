import zmq
from util import svr_util


class MonitorHandler(object):
    def __init__(self, host):
        self._host = host

        self.last_summary = None
        self.last_summary_time = None

        self.last_error = None
        self.last_trace = None
        self.last_error_time = None

        self.start_time = svr_util.get_time()
        self.last_reload_time = svr_util.get_time()

        self._pub_sock = None

    def get_base_info(self):
        base_info = {}

        for k, v in self.__dict__.iteritems():
            if callable(v) or k.startswith('_'):
                continue
            base_info[k] = v

        return base_info

    def set_err(self, ex, trace):
        self.last_error = ex
        self.last_trace = trace
        self.last_error_time = svr_util.get_time()

    def bind(self):
        ctx = zmq.Context.instance()
        self._pub_sock = ctx.socket(zmq.PUB)
        self._pub_sock.bind(self._host)

    def send(self, conf):
        self._pub_sock.send_pyobj((self.get_base_info(), conf))

    def close(self):
        self._pub_sock.close()

    @classmethod
    def instance(cls, conf, old=None):
        new = MonitorHandler(conf['svr.monitor.host'])

        if old:
            old.close()
            new.start_time = old.start_time

        new.bind()
        return new


if __name__ == '__main__':
    h = MonitorHandler({'svr.monitor.host': 'tcp://127.0.0.1:5558'})
    print h.get_base_info()

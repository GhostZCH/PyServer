import time
from server_base import ServerBase


class TestServer(ServerBase):
    def __init__(self):
        ServerBase.__init__(self)

    def on_reload(self):
        self.info('reload')

    def on_start(self):
        self.info('start')

    def on_close(self):
        self.err('close')

    def run(self):
        self.info('run')
        while True:
            print(self.conf['other.x'])
            time.sleep(1)

if __name__ == '__main__':
    svr = TestServer()
    svr.start()


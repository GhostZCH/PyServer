import sys

from util import my_handler

from bin.tiny_svr import TinyServer


class MyServer(TinyServer):
    def __init__(self, url):
        self._url = url
        self._handler = None

    def on_reload(self):
        reload(my_handler)
        self._handler.close()
        self._handler = None

    def on_start(self):
        self._handler = my_handler.MyHandler()


if __name__ == '__main__':
    MyServer(sys.argv[1]).forever()

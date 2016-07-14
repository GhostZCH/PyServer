import sys

from util import example_util
from util import example_handler

from bin.tiny_svr import TinyServer
from util.example_handler import ExampleHandler


class ExampleServer(TinyServer):
    """
    This server class should be very simple.
    Let handler do the business cause it can be reload
    """
    def __init__(self, url):
        self._url = url
        TinyServer.__init__(self)
        # Should not use any other resources witch need release manually(eg. sockets or files).

    def get_name(self):
        return "%s-%s" % (self._conf['svr.name'], self._url)

    def on_reload(self):
        # reload file other than svr_conf and svr_util
        reload(example_handler)
        reload(example_util)

    def get_handler(self):
        return ExampleHandler(self._url, self._conf, self._logger, self._context)

if __name__ == '__main__':
    ExampleServer(sys.argv[1]).forever()

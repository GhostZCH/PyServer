from bin.tiny_handler import TinyHandler


class MyHandler(TinyHandler):
    def __init__(self, argv, config, logger, context, server):
        TinyHandler.__init__(self, argv, config, logger, context, server)
        self._summary = MySummary()

    def run(self):
        self.info('run')

    def get_name(self):
        return

    def get_summary(self):
        return

    def on_start(self):
        TinyHandler.on_start(self)

    def on_close(self):
        pass

    def on_error(self, ex, trace):
        pass

    def on_timer(self, key):
        pass
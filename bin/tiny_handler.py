class TinyHandler:
    def __init__(self, conf, logger, ):
        self.conf = conf

        self.logger = logger
        self.info = logger.info
        self.warn = logger.warn
        self.error = logger.error

    def run(self):
        pass

    def get_summary(self):
        return self.conf

    def get_name(self):
        return self.conf["svr.name"]

    def on_start(self):
        pass

    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_error(self):
        pass

    def on_timer(self, key):
        pass

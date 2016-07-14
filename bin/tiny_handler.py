class TinyHandler:
    def __init__(self, argv, config, logger, context, server):
        self.argv = argv
        self.server = server
        self.config = config
        self.context = context

        self._set_logger(logger)

    def run(self):
        self.info(self.get_summary())
        self.server.running_report()

    def get_summary(self):
        return ''

    def get_name(self):
        return self.config["svr.name"]

    # events
    def on_start(self):
        if self.config['svr.log_conf_on_reload']:
            self.warn(self.config)

    def on_close(self):
        pass

    def on_error(self, ex, trace):
        self.error(ex)
        self.warn(ex)
        self.warn(trace)

    def on_timer(self, key):
        pass

    def _set_logger(self, logger):
        self.logger = logger
        self.info = logger.info
        self.warn = logger.warn
        self.error = logger.error

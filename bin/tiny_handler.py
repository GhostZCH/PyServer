class TinyHandler:
    def __init__(self, config, logger, context):
        self._config = config
        self._context = context
        self._set_logger(logger)

        if self._config['svr.log_conf_on_reload']:
            self.warn(self._config)
            self.warn(self._context)

        self.warn('TinyHandler.init finish')

    def run(self):
        raise NotImplementedError()

    def get_summary(self):
        raise NotImplementedError()

    # events
    def start(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def on_except(self, ex, trace):
        self.error(ex)
        self.warn(ex)
        self.warn(trace)
        return False

    def on_timer(self, key):
        self.info('TinyHandler.on_timer: %s' % key)

    def _set_logger(self, logger):
        self._logger = logger
        self.info = logger.info
        self.warn = logger.warn
        self.error = logger.error

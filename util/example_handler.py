import datetime
from bin.tiny_handler import TinyHandler

from util import example_util


class ExampleHandlerSummary:
    def __init__(self):
        self.run_count = 0
        self.href_count = 0

    def run(self, href_count):
        self.run_count += 1
        self.href_count = href_count

    def __str__(self):
        return 'run_count: %s, href_count: %s' % (self.run_count, self.href_count)


class ExampleHandler(TinyHandler):
    def __init__(self, url, config, logger, context):
        TinyHandler.__init__(self, config, logger, context)

        self._file = None
        self._file_name = self._config['example.handler.filename'] % url
        self._url = 'http://%s/' % url
        self._summary = context(['summary']) if 'summary' in context else ExampleHandlerSummary()

    def run(self):
        self.info('run')
        content = example_util.get_page_content(self._url)
        href_list = example_util.get_page_href_list(content)

        self._file.write(datetime.datetime.now().strftime('%D %H:%M:%S') + '\n')
        self._file.write('\n'.join(href_list))
        self._file.write('\n\n')

        self._summary.run(len(href_list))

    def get_summary(self):
        return str(self._summary)

    def start(self):
        self.warn('ExampleHandler.start')
        self._file = open(self._file_name, 'a')

    def close(self):
        self.warn('ExampleHandler.close')
        self._file.close()

    def on_except(self, ex, trace):
        """
        :return: True: keep going, False: exit process
        """
        self.warn(ex)
        self.warn(trace)
        return True

    def on_timer(self, key):
        TinyHandler.on_timer(self, key)


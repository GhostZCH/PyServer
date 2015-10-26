import time

from bin.svr_base import ServerBase

from conf import my_conf
from util import my_util


class MyServer(ServerBase):
    def __init__(self):
        ServerBase.__init__(self)

        # you can init attributes here
        self.input_file = None
        self.output_file = None

    def on_reload(self):
        self.info('reload')

        # you can reload your own config or code here
        # use kill -2 to reload code
        # you need NOT to restart when you want to update them
        # I suggest you can write most code in other py files so you can do 'hot-update'

        reload(my_util)
        reload(my_conf)

    def on_start(self):

        self.info('start: s%', self.name)

        # you can init your param here. like files, sockets...
        self.input_file = open(my_conf.CONFIG_DICT['in'], 'r')
        self.output_file = open(my_conf.CONFIG_DICT['out'], 'w')

    def on_close(self):
        self.err('close')

        # close you need to close, especially init in function on_start
        self.input_file.close()
        self.output_file.close()

    def on_except(self, ex):
        # handle except, you can close program or just log it
        self.err(ex)

        # if call close() it while call on_close automatic
        self.close(delay=1, exit_code=-2)

    def run(self):
        self.info('run')

        while True:
            x = self.conf['other.x']

            for line in self.input_file:
                result = my_util.my_operation(line, x)
                self.output_file.write(result)

                self.info(result)

            self.input_file.seek(0)
            self.output_file.seek(0)

            time.sleep(1)

if __name__ == '__main__':
    svr = MyServer()
    svr.start()
    # svr.forever() run forever
    # svr.close()  close manually


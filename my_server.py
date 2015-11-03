# -*- coding: utf-8 -*-

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
        self.info('on_reload')

        # you can reload your own config or code here
        # use kill -2 to reload code
        # you need NOT to restart when you want to update them
        # I suggest you can write most code in other py files so you can do 'hot-update'

        reload(my_util)
        reload(my_conf)
        self.on_close()
        self.on_start()

    def on_start(self):
        self.info('start')

        # you can init your param here. like files, sockets...
        self.input_file = open(my_conf.CONFIG_DICT['in'], 'r')
        self.output_file = open(my_conf.CONFIG_DICT['out'], 'w')

    def on_close(self):
        self.warn('on_close')

        # close you need to close, especially init in function on_start
        if self.input_file:
            self.input_file.close()
            
        if self.output_file:
            self.output_file.close()
        
        self.input_file = None
        self.output_file = None

        self.warn('on_close_over')

    def on_except(self, ex, trace_back):
        # handle except, you can close program or just log it
        self.err(ex)
        self.warn(trace_back)

        # if call close() it while call on_close automatic
        self.close(delay=1, exit_code=-2)

    def run(self):
        self.info('run')

        x = self.conf['other.x']

        msg = self.input_file.read()
        result = my_util.my_operation(msg, x)
        self.output_file.write(result)

        self.info('%s - > %s' % (msg, result))

        self.input_file.seek(0)
        self.output_file.seek(0)

        self.info('run over')

if __name__ == '__main__':
    svr = MyServer()
    # svr.start()
    svr.forever()  # run forever
    # svr.close()  close manually


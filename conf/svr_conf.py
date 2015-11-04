# -*- coding: utf-8 -*-

CONFIG_DICT = {
    # server
    'svr.name': 'my_server',
    'svr.log_conf_on_reload': True,

    # timer 设置 (单位:s)
    'svr.timer.min_span': 1,  # timer的精度
    'svr.timer.run_status_check_time_span': 60,  # 最大无响应时间，超过这个时间没有相应，自动退出
    'svr.timer.summary_output_time_point': 'M',  # 报告输出类型 D(per day), H(per hour), M(per minute)

    # close 信号处理配置
    'svr.close.wait_lock_delay': 1,
    'svr.close.force_close_delay': 10,

    # log
    'log.level': 'INFO',
    'log.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
    'log.console.level': 'INFO',  # todo
    'log.syslog.level': 'WARN',   # todo

    # other
    'other.x': 3
}

# Tiny

![](http://img0.pcgames.com.cn/pcgames/1112/13/2382339_130224659.jpg)

一个针对Linux的轻量级python服务器架构，提供服务器需要一些基本功能，诸如：热更新、安全退出、日志处理、定时器、运行状态统计和监控等。尽可能的简单，只要最实用的功能，代码总量控制在1k内。和supervise工具协同，效果更佳

## features

### basic

#### 代码结构

+ my_*.py 是本框架的示例

+ svr_*.py 是本框架的源代码


#### 使用方式

开发人员通过继承ServerBase得到基本功能，如：

    from bin.svr_base import ServerBase
    
    class MyServer(ServerBase):
    
ServerBase 提供一些抽象函数供开发者实现自定义的处理：

    # ------------- abstract function --------------
    def on_reload(self):
        pass

    def on_close(self):
        pass

    def on_start(self):
        pass

    def on_except(self, ex, trace_back):
        pass

    def get_summary(self):
        pass

    def run(self):
        pass
        

**备注：可参照 my_server.py** 

### hot-update

  `./svr.sh reload`
  
### safe-close

+  `./svr.sh close`
+  `ctrl+C`
  
### logs

调用方式：

 +   self.info()  建议打印正常的运行信息，方便调试, 上线产品不打印，默认只输出控制台
 +   self.warn()  系统运行的关键节点(启动，重启)，对程序运行有可能产生影响的事件，捕获的不影响程序正常的异常，默认输出控制台和syslog
 +   self.err()   严重的错误，可能直接导致程序退出的异常，默认输出控制台和syslog，建议设置邮箱自动发送该级别的log

提供3种log方式，后面会增加email，参见 conf/svr_conf.py

    CONFIG_DICT = {
        # ....
    
        # log
        'log.console': True,
        'log.console.level': 'INFO',
        'log.console.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
    
        'log.syslog': True,
        'log.syslog.level': 'WARN',
        'log.syslog.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
    
        'log.file_log': '/home/ghost/code/log/my_svr.log',
        'log.file_log.level': 'WARN',
        'log.file_log.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
    }


### timer

通过调用`add_timer` 和 `remove_timer`增加和减少timer，timer之间是串行的，不需要用锁，timer和run之间的锁需要开发者根据需求自己处理。已实现如下timer:

+ PeriodTimer 周期定时器
+ FixedPeriodTimer 固定时间点的定时器，每小时/每天/每分钟执行
+ 可以继承 _AbstractTimer 实现新的定时器（见 PyServer/bin/svr_timer.py）


通过配置调整timer精度：

        CONFIG_DICT = {
            ....
            
            # timer 设置 (单位:s)
            'svr.timer.min_span': 1,  # timer的精度
            
            ....
        }

### summary & auto-exit

+ 超过一定时间没有调用`running_report` 函数，认为程序挂死，自动退出
+ 每隔一定时间自动调用`get_summmary` 函数，将返回结果输出到日志中


        CONFIG_DICT = {
            ...
            
            # timer 设置 (单位:s)
            'svr.timer.min_span': 1,  # timer的精度
            'svr.timer.run_status_check_time_span': 60,  # 最大无响应时间，超过这个时间没有相应，自动退出
            'svr.timer.summary_output_time_point': 'M',  # 报告输出类型 D(per day), H(per hour), M(per minute)
        
            ...
        }


### monitor api

使用zmq PUB-SUB 模式定时输出运行信息，通过如下参数配置

        CONFIG_DICT = {
            ...
            
            'svr.monitor': True,
            'svr.monitor.timer': 10,
            'svr.monitor.host': 'tcp://127.0.0.1:5558',
        
            ...
        }
        
        
可以通过 zmq.Socket.recv_pyobj() 方法接收数据， 详见：[Tiny_monitor](https://github.com/GhostZCH/Tiny_monitor)

数据格式如下：

        (base_info_dict, svr_conf_dict)

+ base_info_dict(程序运行基本信息)：

        {'last_error': None,
         'last_error_time': None,
         'last_reload_time': '2015/11/18 22:21:42',
         'last_summary': 'run count = 28',
         'last_summary_time': '2015/11/18 22:24:01',
         'last_trace': None,
         'start_time': '2015/11/18 22:21:42'}
         
+ svr_conf_dict(**正在**使用配置):

        {'log.console': True,
         'log.console.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
         'log.console.level': 'INFO',
         'log.email': False,
         'log.email.config': {'from': ('xxx@163.com', 'xxx'),
                              'host': ('smtp.163.com', 25),
                              'target': ['xxx@163.com']},
         'log.email.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
         'log.email.level': 'ERROR',
         'log.file_log': '/home/ghost/code/log/my_svr.log',
         'log.file_log.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
         'log.file_log.level': 'WARN',
         'log.syslog': True,
         'log.syslog.format': '<%(levelname)s: %(name)s(%(process)d)> [%(filename)s: %(lineno)d] >> %(message)s ',
         'log.syslog.level': 'WARN',
         'other.x': 3,
         'svr.close.force_close_delay': 10,
         'svr.close.wait_lock_delay': 1,
         'svr.log_conf_on_reload': True,
         'svr.monitor': True,
         'svr.monitor.host': 'tcp://127.0.0.1:5558',
         'svr.monitor.timer': 10,
         'svr.name': 'my_server',
         'svr.timer.min_span': 1,
         'svr.timer.run_status_check_time_span': 60,
         'svr.timer.summary_output_time_point': 'M'}


## tasks

### done

+ 动态更新代码和配置 `svr.sh reload`
+ 安全退出 `svr.sh close`
+ syslog, consolelog日志处理
+ 多种类型timer
+ 周期性输出统计信息
+ 邮件通知
+ 一定时间不响应，自动退出
+ 错误统一处理
+ 输出日志到特定目录
+ 不同日志不同级别
+ 自动生成重启和关闭脚本 svr.sh
+ 定时输出运行情况到zmq,用多种moniter监控

### todo

+ 写注释，更新readme !!!
+ timeout task
+ retry task
+ 更新需要用锁
+ checkpoint(LATER)
+ master-slave(LATER)

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

  `./svr.sh close`
  `ctrl+C`
  
### logs

调用方式：

    self.info()
    self.warn()
    self.err()

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




## tasks

### done

+ 动态更新代码和配置 `svr.sh reload`
+ 安全退出 `svr.sh close`
+ syslog, consolelog日志处理
+ 多种类型timer
+ 周期性输出统计信息
+ 一定时间不响应，自动退出
+ 错误统一处理
+ 输出日志到特定目录
+ 不同日志不同级别
+ 自动生成重启和关闭脚本 svr.sh
+ 
### todo

+ 写注释，更新readme !!!
+ timeout task
+ retry task
+ 更新需要用锁

+ checkpoint(LATER)
+ 邮件通知(LATER)
+ master-slave(LATER)


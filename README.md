# PyServer

一个针对Linux的轻量级python服务器架构，提供服务器需要一些基本功能，诸如：热更新、安全退出、日志处理、定时器、运行状态统计和监控等。尽可能的简单，只要最实用的功能，代码总量控制在1k内。

## features

### basic

my_*.py 是本框架的示例
svr_*.py 是本框架的源代码


### hot-update
  kill -10
  
### safe-close
  ctrl+C
  kill

### logs



## tasks

### done

+ 动态更新代码和配置 kill -10
+ 安全退出 kill -2
+ syslog, consolelog日志处理
+ 多种类型timer
+ 周期性输出统计信息
+ 一定时间不响应，自动退出
+ 错误统一处理
+ 输出日志到特定目录(IMPORTENT)
+ 不同日志不同级别(IMPORTENT)

### todo
+ timeout task
+ 更新需要用锁
+ 自动生成重启和关闭脚本
+ checkpoint(LATER)
+ 邮件通知(LATER)
+ master-slave(LATER)



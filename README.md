# PyServer

抽象服务程序原型, 提供一些基本功能：

## done

+ 动态更新代码和配置 kill -10
+ 安全退出 kill -2
+ syslog, consolelog日志处理
+ 测试热替换
+ 调整目录结构
+ 多种类型timer，(相对定时，绝对定时)(IMPORTENT)
+ 周期性输出统计信息(IMPORTENT)
+ 一定时间不响应，自动退出

## todo
+ 输出日志到特定目录(IMPORTENT)
+ 不同日志不同级别(IMPORTENT)
+ 更新需要用锁
+ 自动生成重启和关闭脚本
+ checkpoint(LATER)
+ 邮件通知(LATER)
+ master-slave(LATER)



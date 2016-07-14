#!/bin/bash

ARGV='argv'
SVR_NAME='svr-name'
PID_FILE_NAME=${SVR_NAME}-${ARGV}.pid

work_dir=`dirname $(realpath $0)`
cd ${work_dir}

if [ "$1" == "reload" ]; then
    pid=`cat ${PID_FILE_NAME}`
    echo pid = ${pid} reloading...
    kill -10 ${pid}
elif [ "$1" == "close" ]; then
    pid=`cat ${PID_FILE_NAME}`
    echo pid = ${pid} close...
    kill -15 ${pid}
elif [ "$1" == "run" ]; then
    python example_svr.py ${ARGV}
else
    echo unknown cmd use 'reload', 'close' or 'run'
fi

#!/bin/bash

pwd=`dirname $(realpath $0)`

echo ${pwd}


if [ "$1" == "reload" ]; then
    pid=`cat svr.pid`
    echo pid = ${pid} reloading...
    kill -10 ${pid}
elif [ "$1" == "close" ]; then
    pid=`cat svr.pid`
    echo ${pid} = ${pid} close...
    kill -15 ${pid}
elif [ "$1" == "run" ]; then
    echo start...
    python svr.py my-svr-name
else
    echo unknown cmd use 'reload', 'close' or 'run'
fi
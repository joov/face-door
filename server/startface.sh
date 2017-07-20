#!/bin/bash
/usr/bin/nohup /usr/bin/python3 face.py -start > /var/log/face.log 2>&1 &
echo $! > /var/run/face.pid
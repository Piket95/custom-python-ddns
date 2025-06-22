#!/bin/sh
/usr/sbin/named -c /etc/bind/named.conf
python main.py
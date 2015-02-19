#!/bin/bash

SPEEDTEST=speedtest_cli.py
# 5754) Fastmetrics Inc. (San Francisco, CA, United States) [4.34 km]
# 1749) Monkey Brains (San Francisco, CA, United States) [4.44 km]
# 603) Unwired (San Francisco, CA, United States) [4.44 km]
# 1783) Comcast (San Francisco, CA, United States) [4.44 km]

FASTMETRICS=5754
MONKEYBRAINS=1749
UNWIRED=603
COMCAST=1783

LOGFILE=$1
NICMP=200

while true
do
    echo "--------" >> $LOGFILE
    date >> $LOGFILE
    echo "IPv4 ping N=$NICMP to kernel.org" >> $LOGFILE
    ping -c $NICMP kernel.org | tail -n 3 >> $LOGFILE
    echo "IPv6 ping N=$NICMP to kernel.org" >> $LOGFILE
    ping6 -c $NICMP kernel.org | tail -n 3 >> $LOGFILE
    echo "Speedtest to Fastmetrics SF" >> $LOGFILE
    python $SPEEDTEST --server $FASTMETRICS >> $LOGFILE
    sleep 900
done

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

UBUNTU_MIRROR="http://mirrors.cat.pdx.edu/ubuntu-releases/14.04.1/ubuntu-14.04-server-amd64.iso"
NBYTES=40000000

LOGFILE=$1
NICMP=200

while true
do
    date
    echo "--------" >> $LOGFILE
    date >> $LOGFILE
    echo -n "Webpass IP:" >> $LOGFILE
    curl -s ip.webpass.net | grep '<h1>' | cut -f2 -d\> | cut -f1 -d\< >> $LOGFILE
    echo "IPv4 ping N=$NICMP to kernel.org" >> $LOGFILE
    ping -c $NICMP kernel.org | tail -n 3 >> $LOGFILE
    echo "IPv6 ping N=$NICMP to kernel.org" >> $LOGFILE
    ping6 -c $NICMP kernel.org | tail -n 3 >> $LOGFILE
    echo "Speedtest to Fastmetrics SF" >> $LOGFILE
    python $SPEEDTEST --server $FASTMETRICS >> $LOGFILE
    echo "Download $NBYTES of Ubuntu ISO from PDX mirror over IPv4" >> $LOGFILE
    curl -4sr 0-$((NBYTES-1)) $UBUNTU_MIRROR | dd of=/dev/null 2>&1 | tail -n 1 >> $LOGFILE
    echo "Download $NBYTES of Ubuntu ISO from PDX mirror over IPv6" >> $LOGFILE
    curl -6sr 0-$((NBYTES-1)) $UBUNTU_MIRROR | dd of=/dev/null 2>&1 | tail -n 1 >> $LOGFILE
    sleep 600
done

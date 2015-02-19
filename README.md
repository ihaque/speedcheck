# speedlog

Leave `speedtest.sh logfile` running in a terminal in the background and it'll
check packet loss and throughput about every 20 minutes.

`python parse_logfile.py < logfile > log.tsv` to convert the logfile to
tab-separated text that can then be easily loaded into whatever for plotting

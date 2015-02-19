IPV4 = 1
IPV6 = 2
DOWN = 3
UP = 4

from sys import stdin
from re import search

def compute_loss(loss_line):
    fields = loss_line.split()
    xmit = float(fields[0])
    recv = float(fields[3])
    return '%.1f %%' % (100 * (xmit - recv) / float(xmit))

def parse_entry(lines):
    loss_lines = [line for line in lines
                  if search('% packet loss', line)]
    rtt_lines = [line for line in lines
                 if search('rtt min/avg/max/mdev', line)]
    date = lines[0]
    losses = map(compute_loss, loss_lines)
    rtts = [line.split(' ')[3] for line in rtt_lines]
    try:
        down = next(line for line in lines
                    if line.startswith('Download:')).split(' ')[1]
    except StopIteration:
        down = ''
    try:
        up = next(line for line in lines
                  if line.startswith('Upload:')).split(' ')[1]
    except StopIteration:
        up = ''
    return [date, losses[0], losses[1], down, up, rtts[0], rtts[1]]

entries = []
cur_entry = []
for line in stdin:
    line = line.strip()
    if line == '--------':
        if cur_entry:
            entries.append(cur_entry)
            cur_entry = []
    else:
        cur_entry.append(line)

print '\t'.join(['Date', 'IPv4 loss', 'IPv6 loss',
                 'IPv4 min/avg/max/mdev', 'IPv6 min/avg/max/mdev',
                 'Down Mbit/s', 'Up Mbit/s'])
for entry in entries:
    print '\t'.join(parse_entry(entry))

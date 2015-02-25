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


def parse_loss_rtt(lines, start_line):
    def _valid():
        if not lines[start_line].endswith('to kernel.org'):
            return False
        if len(lines) < (start_line + 4):
            return False
        if not search(r'packets transmitted.*received.*packet loss',
                      lines[start_line + 2]):
            return False
        if not lines[start_line + 3].startswith('rtt min/avg/max'):
            return False
        return True

    if not _valid():
        return '', ''
    loss = compute_loss(lines[start_line + 2])
    rtt = lines[start_line + 3].split(' ')[3]
    return loss, rtt


def parse_entry(lines):
    date = lines[0]

    try:
        ipv4_icmp_index = next(i for i, line in enumerate(lines)
                               if line.startswith('IPv4 ping'))
        ipv4_loss, ipv4_rtt = parse_loss_rtt(lines, ipv4_icmp_index)
    except StopIteration:
        ipv4_loss, ipv4_rtt = '', ''

    try:
        ipv6_icmp_index = next(i for i, line in enumerate(lines)
                               if line.startswith('IPv6 ping'))
        ipv6_loss, ipv6_rtt = parse_loss_rtt(lines, ipv6_icmp_index)
    except StopIteration:
        ipv6_loss, ipv6_rtt = '', ''

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

    try:
        ipv4_index = next(i for i, line in enumerate(lines)
                          if line.endswith('mirror over IPv4'))
        ipv4_line = lines[ipv4_index + 1]
        fields = ipv4_line.split(' ')
        mbits = float(fields[0]) * 8 * 1e-6
        secs = float(fields[5])
        ipv4_iso_down = str(mbits/secs)
    except (StopIteration, IndexError):
        ipv4_iso_down = ''

    try:
        ipv6_index = next(i for i, line in enumerate(lines)
                          if line.endswith('mirror over IPv6'))
        ipv6_line = lines[ipv6_index + 1]
        fields = ipv6_line.split(' ')
        mbits = float(fields[0]) * 8 * 1e-6
        secs = float(fields[5])
        ipv6_iso_down = str(mbits/secs)
    except (StopIteration, IndexError):
        ipv6_iso_down = ''

    return [date, ipv4_loss, ipv6_loss, down, up,
            ipv4_iso_down, ipv6_iso_down,
            ipv4_rtt, ipv6_rtt]

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
                 'speedtest.net Down Mbit/s', 'speedtest.net Up Mbit/s',
                 'PDX IPv4 Down Mbit/s', 'PDX IPv6 Down Mbit/s',
                 'IPv4 min/avg/max/mdev', 'IPv6 min/avg/max/mdev', ])
for entry in entries:
    print '\t'.join(parse_entry(entry))

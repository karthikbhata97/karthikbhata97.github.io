---
layout: post
title: "InCTF load3r writeup"
categories: ctf
---

This is a writeup for the Reversing challenge `load3r` from [InCTF-2018](https://ctf.inctf.in/). 

* Checkout the binary [here](/data/load3r/boot_try.bin).
* Here is the solution in python: [solve.py](/data/load3r/solve.py)
* Here is the analyzed disassembly: [dump](/data/load3r/dump)

Problem statement:
```
======= Difficulty level : Easy ========

A basic bootloader challenge. Note: The flag format is inctf{correct_input}

Note: The challenge must be run in qemu-system-i386 version 2.5.0

========== Authors : b3y0nd3r, r00tus3r ==========

```

It says it's a bootloader challenge. When we run `file` command on it,
```
$ file boot_try.bin
boot_try.bin: DOS/MBR boot sector
```

We should know that when the when x86 machine boots, it begins execution in [`real mode`](https://wiki.osdev.org/Real_Mode). This is a 16bit mode, hence the binary should be disassembled in 16 bit mode. I used `objdump` to get the disassembly.
```
objdump -D -b binary -mi386 -Maddr16,data16 boot_try.bin -Mintel > dump
```
This got me disassembly in the `dump` file.

This also gave me some extra disassembly which were actually strings. Thus I had to cleanup a bit. Also I used [this](http://www.ablmcc.edu.hk/~scy/CIT/8086_bios_and_dos_interrupts.htm) website to do a quick search about interrupts.
I used radare2 as a hex reader, which helped me seek to address with `s addr` command and print hex using `px` command.

[This](/data/load3r/dump) is the final dump file where I took notes on.

## Let's analyze the disassembly
#### 0x00
- At address 0x00, main code which sets up registers and calls `0x11b` with si value set to `0x16`
- At `0x16` string, `ENTER THE FLAG` exists. Thus it is calling print function.
![Enter the flag](/data/load3r/enter_the_flag.png)
- After that it calls `0x128`.

#### 0x11b
- This is a print function to the address pointed by si. Observe it calls interrupt `int 0x10` with ah=0xe.

#### 0x128
- Here it takes input from keyboard.  Observe `int 0x16`.
- It reads only 0x22 characters or until '\r'
- Input is stored at `0x6f`

#### 0x154
- This does first round of encryption.
- Based on string at `0xc9` i.e '0100010011011101111111011010110101', at the offset if it's '1', it byte is shifted left by one bit (shl al, 1) else shifted right by one bit (shr al, 1).
![0101 string](/data/load3r/01010.png)
- The result is stored in 0xee.
- Remember it considers only 0x22 characters.

#### 0x184
- It calls print with argument (si pointing) to the string 'NOOOO'

#### 0x192
- It calls print with argument (si pointing) to the string 'Yeah, that is the flag'

#### 0x1a8
- This does second round of encryption.
- It XORs each byte from previous round's result stored at 0xee with value `0x5`.
- Then it compares with the string at 0x27 in reverse order.
- At 0x27, the string 'w2g1kS<c7me3keeuSMg1kSk%Se<=S3%/e/' exists.
- If matches calls `0x192` else calls `0x184`

## Solution.
* Take the string `w2g1kS<c7me3keeuSMg1kSk%Se<=S3%/e/` and flag `0100010011011101111111011010110101`.
* XOR each character with `0x5` and store this new string.
* Reverse this new string.
* Based on the flags character at each characters offset,
  ```
    if flag_char == '1':
        right shift the bits of character by one bit.
    else:
        left shift the bits of character by one bit
  ```
* The flag is the resulting string. (Enclosed by the inctf{FLAG})

Checkout this solution written in python.
[solve.py](/data/load3r/solve.py)
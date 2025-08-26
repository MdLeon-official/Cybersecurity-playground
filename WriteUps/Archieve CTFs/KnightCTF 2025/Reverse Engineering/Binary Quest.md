### Binary Quest

First, I ran the `strings` command on the binary (`strings binary_quest`) and noticed a line saying:
`This file is packed with the UPX executable packer`.

So, I unpacked it with:

```
upx -d binary_quest
```

After that, I opened the unpacked file in **Ghidra**. Inside the function `FUN_001010a0()`, I found the main logic. There was a line:

```c
iVar1 = strcmp(local_58, local_98);
```

Here, `local_98` was assigned a hex string: `0x7334655f*7****73`.

I decoded that hex string, which revealed a piece of the flag. Then I noticed two more hex-encoded values (`0x34575f7b4****34b` and `0x7d5f3f**`). Decoding those gave me the remaining parts of the flag.

Finally, combining all three decoded pieces revealed the complete flag.


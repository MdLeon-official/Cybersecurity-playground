# Riyadh

To solve this challenge I used gdb and ghidra. First open the challenge file with ghidra and I analyze the decompiling code.
Then I opened the file with gdb.

First I used ```disassemble main```. At main+96 I saw that the strcmp function was called. I set a breakpoint there.
```break *main+96``` and then I used ```run hi``` to see what strcmp function comparing with. I found the flag but IT WAS A FAKE FLAG :').

Then I saw the decompiling code in ghidra again and saw the else condition. Inside this else condition theres a if condition that comparing
a string with a length of 30. 

So I set a breakpoint there `break *main+151`. Used `run CTFLearn{aaaaaaaaaaaaaaaaaaaa}`. And it gave me the actual flag.

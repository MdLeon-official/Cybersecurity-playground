# picoGym Exclusive
1. **Picker I**
   analyze the code -> call win instead of getRandomNumber

2. **Picker II**
   Had to exploit the eval() function since Ii evaluates the string expression given to it and displays the result -> used `print(open('flag.txt', 'r').read())`

3. **Picker III**
   Analyze the code -> overwrite read_variable to win

4. **GDB baby step 1**
   `gdb ./file -> b main -> run -> next -> next .... -> info register -> x/o $rax`

5. **GDB baby step 2**
   same as GDB baby step 1

6. **GDB baby step 3**
   gdb ./file -> disas main ->
   ```
   0x0000000000401115 <+15>:	mov    DWORD PTR [rbp-0x4],0x2262c96b
   0x000000000040111c <+22>:	mov    eax,DWORD PTR [rbp-0x4]
   ```
-> b *0x000000000040111c -> run -> x/4xb $rbp-0x4 (since after that breakpoint 0x2262c96b goes to rbp-0x4)

7. **GDB baby step 4**
	info functions -> func1 -> disas func1 -> `0x0000000000401114 <+14>:	imul   eax,eax,0x3269`

8. **ASCII FTW**
   gdb -> disas main

9. **Bit-O-Asm-1** : analyze asm
10. **Bit-O-Asm-2** : analyze asm
11. **Bit-O-Asm-3** : analyze asm
12. **Bit-O-Asm-4** : analyze asm


# 2019
1. **vault-door-training**
   Java

2. **vault-door-1**
   Java code organize

3. **vault-door-3**
```
s = "jU5t_a_sna_3lpm13gf49_u_4_m9r540"
password = [""] * 32
for i in range(8):
    password[i] = s[i]
for i in range(8, 16):
    password[23 - i] = s[i]
for i in range(16, 32, 2):
    password[46 - i] = s[i]
for i in range(31, 16, -2):
    password[i] = s[i]
print("".join(password))
```


4. **vault-door-4**
```
import codecs
ascii = [106 , 85  , 53  , 116 , 95  , 52  , 95  , 98]
hex = [0x55, 0x6e, 0x43, 0x68, 0x5f, 0x30, 0x66, 0x5f]
octal = [0o142, 0o131, 0o164, 0o63 , 0o163, 0o137, 0o142, 0o64]
normal = ['e' , '9' , '4' , '3' , 'c' , '3' , 'a' , '0']
my_bytes = bytes(ascii + hex + octal)
s = ''
s = s.join([chr(i) for i in my_bytes])
for i in normal:
    s += i
# s = s.join(normal)
print(s)
```

5. **vault-door-5**
```
import base64
from urllib.parse import unquote
expected = "JTYzJTMwJTZlJTc2JTMzJTcyJTc0JTMxJTZlJTY3JTVm"+ "JTY2JTcyJTMwJTZkJTVmJTYyJTYxJTM1JTY1JTVmJTM2"+ "JTM0JTVmJTM0JTMxJTM4JTM1JTM1JTM1JTMxJTY1"
b64 = base64.b64decode(expected).decode()
print(unquote(b64))
```

6. **vault-door-6**
```
myBytes = [
            0x3b, 0x65, 0x21, 0xa , 0x38, 0x0 , 0x36, 0x1d,
            0xa , 0x3d, 0x61, 0x27, 0x11, 0x66, 0x27, 0xa ,
            0x21, 0x1d, 0x61, 0x3b, 0xa , 0x2d, 0x65, 0x27,
            0xa , 0x6d, 0x64, 0x30, 0x6d, 0x30, 0x62, 0x6c,
        ]
myString = ""
for i in range(0,32):
    myString += chr(myBytes[i] ^ 0x55)
print(myString)
```

7. **vault-door-7**



# 2022
1. **unpackme**
upx -d filename
opened with ghidra to get the secret number
Using gdb-gef:
```
gdb -q ./unpackme-upx
disas main
# note cmp $0xb83cb, %eax and call rotate_encrypt - decode this hex: 0xb83cb (754635)
b *0x401ee0
run
# input: 754635
x/s $rax
```

2. **GDB Test Drive**
```
$ chmod +x gdbme
$ gdb gdbme
(gdb) layout asm
(gdb) break *(main+99) // a sleep function was being called
(gdb) run
(gdb) jump *(main+104) // using this ignore that sleep function
```

3. **Wizardlike**

Method 1: Using ghidra + gHex
Found the logic using ghidra and then Tampered the logic by editing hex with gHex - [Video](https://www.youtube.com/watch?v=1iWkFelUs_k)

Method 2: 
```
Radare 2 Guide:
r2 -d[debug] -w[write on it] -A[Analyze it]
? [ask for help]
a? [commands starts with a]
aa? [commands starts with aa]
aaa? [commands starts with aaa]
afl [all function list]
s entry0 [seek to entry0 func]
V [It'll visualize what is going on]
p [different view - only assembly code]
another p [stack, register and assembly code]
another p [representation of functions and bytes]
another p [maybe readable strings idk]
VV [Graph / Flow chart view]

```

4. **KeyGenMe**




# 2023
1. **Virtual Machine 0**
Totally new types of problem. Had to analyze a Collada (.dae) file. Convert to 3D using this website: [Link](https://3dviewer.net/index.html)

2. 

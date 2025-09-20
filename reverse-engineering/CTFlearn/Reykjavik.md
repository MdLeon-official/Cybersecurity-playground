# Reykjavik

### **Way 1:**
Use `ltrace ./Reykjavik "CTF"` and You will get the flag.

### **Way 2: (with gdb):**
```gdb
disassemble main
```
You will see that there is a call to strcmp at `main+200`. Set a breakpoint there:
```gdb
break *main+200
```
After that use: 
```gdb
run 'CTF'
```
You will see that the first argument of strcmp is at $rdi. So:
```gdb
x/s $rdi
```
You will get the flag.

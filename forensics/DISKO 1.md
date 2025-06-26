## [DISKO 1](https://play.picoctf.org/practice/challenge/505?category=4&page=1)

#### 🧪 Steps to Solve:

1. Downloaded the `disko-1.dd` file from the challenge.
2. Ran the following command to extract readable ASCII strings:

   ```bash
   strings disko-1.dd | grep pico
   ```
3. Found the flag directly in the output.

#### 🏁 Flag:

```
picoCTF{1t5_ju5t_4_5tr1n9_e3408eef}
```

#### Key Notes:
- *strings is a basic but powerful command to extract ASCII text from binary files.*
- *Disk images often contain hidden flags as strings or metadata.*
- *Grep helps narrow down possible flags quickly when you know the prefix*

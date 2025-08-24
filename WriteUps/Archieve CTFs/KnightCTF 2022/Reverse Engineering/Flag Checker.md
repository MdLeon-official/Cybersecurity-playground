### Flag Checker

1. **Download** the challenge executable (`chmod +x filename`).
2. **Open in Ghidra** and locate the `main` function. The program stores an encoded string:

   ```c
   builtin_strncpy(local_48,"08'5[Z'Y:H3?X2K3V)?D2G3?H,N6?G$R(G]",0x24);
   ```
3. That program 
   * Reads the user input (flag).
   * Transforms each character with a custom formula depending on whether it’s uppercase, lowercase, or other.
   * Applies an additional shift to all characters.
4. **Validation:** Compares the transformed input with the stored encoded string. If it matches, the flag is correct.
5. **Solution:** Reverse the transformations in Python to recover the original flag.
```python
enc = "08'5[Z'Y:H3?X2K3V)?D2G3?H,N6?G$R(G]"

out = []
for ch in enc:
    c1 = (ord(ch) + 0x20) % 256          # undo -0x20
    u = (-0x65 - c1) % 256               # candidate uppercase
    l = (-0x25 - c1) % 256               # candidate lowercase
    if 65 <= u <= 90:
        out.append(chr(u))
    elif 97 <= l <= 122:
        out.append(chr(l))
    else:
        out.append(chr(c1))              # non-letters
print("".join(out))
```

```python
enc = "*9J<qiEUoEkU]EjUc;U]EEZU`EEXU^7fFoU^7Y*_D]s"

password = ""
for ch in enc:
    if ch == '*':
        ch = 'A'
    password += chr(ord(ch) + 10)

print("Recovered password:", password)
```

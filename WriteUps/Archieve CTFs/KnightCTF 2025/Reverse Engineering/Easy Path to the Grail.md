## Easy Path to the Grail


```python
def reverse_bits(b):
    out = 0
    for _ in range(8):
        out = (out << 1) | (b & 1)
        b >>= 1
    return out

hex_string = "D2C22A62DEA62CCE9EFA0ECC86CE9AFA4ECC6EFAC6162C3636CC76E6A6BE"

flag = ""
for i in range(0, len(hex_string), 2):
    byte_val = int(hex_string[i:i+2], 16)   
    orig = reverse_bits(byte_val)
    flag += chr(orig)

print("Recovered flag:", flag)
```



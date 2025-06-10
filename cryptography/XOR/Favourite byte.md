# 🔐 Favourite byte

**Source:** [Cryptohack - General](https://cryptohack.org/challenges/general/)

---

## Challenge Description

For the next few challenges, you'll use what you've just learned to solve some more XOR puzzles.

> I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.

Hex string given:

```
73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d
```

---

## Approach

This is a **single-byte XOR cipher**. The data has been encrypted by XORing each byte of the plaintext with a single repeating byte (the same value across the string). Our job is to:

1. Convert the hex-encoded ciphertext into bytes.
2. Brute-force all 256 possible single-byte keys.
3. XOR the ciphertext with each key and decode the result.
4. Look for human-readable output, specifically something that includes `"crypto{"`.

---

## Tools

* **XOR Cipher** decryption
* **Pwntools** `xor()` function
* **Brute-force** of 256 possible byte values
* **Hex decoding** using `bytes.fromhex()`
* **Python exception handling** to skip invalid decodings

---

## Code

```python
from pwn import xor

data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
fromHexData = bytes.fromhex(data)

for key in range(256):
    decrypted = xor(fromHexData, key)
    try:
        decoded = decrypted.decode()
        if "crypto" in decoded:
            print(f"[+] Key: {key}")
            print(f"[+] Flag: {decoded}")
            break
    except UnicodeDecodeError:
        continue
```

---


**Flag:** `crypto{0x10_15_my_f4v0ur173_by7e}`


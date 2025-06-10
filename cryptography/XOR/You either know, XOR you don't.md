
# You either know, XOR you don't

*Source:* [https://cryptohack.org/challenges/general/](https://cryptohack.org/challenges/general/)

---

## Challenge Description

I've encrypted the flag with my secret key, you'll never be able to guess it.
Remember the flag format and how it might help you in this challenge!

Encrypted hex:

```
0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104
```

---

## Approach

We are given a flag encrypted with a secret repeating key using XOR.
Since all Cryptohack flags begin with `"crypto{"`, we can use this known plaintext to extract the repeating key. This is a **known-plaintext XOR attack**.

Steps:

1. Convert the hex string to bytes.
2. XOR the encrypted bytes with the known plaintext `"crypto{"` to recover the repeating key.
3. Use the recovered key to XOR the entire encrypted message and obtain the full flag.

---

## Tools

* XOR encryption/decryption.
* `pwntools.xor()` — conveniently handles repeating keys.
* Known plaintext attack using flag prefix.
* `bytes.fromhex()` to decode the hex input.

---

## 🔧 Code

```python
from pwn import xor

# Given encrypted flag (hex)
flag = bytes.fromhex('0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104')

# Known flag format
flag_format = "crypto{"
ff_bytes = flag_format.encode()

# Derive the key using known plaintext
key = xor(flag, ff_bytes)

# Try the key
print(xor(flag, key))               # Full flag
print(xor(flag, "myXORkey".encode()))  # Once key is known
```

---

✅ **Output (Flag):**

```
b'crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}'
```


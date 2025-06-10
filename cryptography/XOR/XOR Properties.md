# XOR Properties

*Source:* [https://cryptohack.org/challenges/general/](https://cryptohack.org/challenges/general/)

---

## 📝 Challenge Description

XOR is a bitwise operator that outputs 0 if both input bits are the same, and 1 otherwise. It’s denoted by ⊕ in theory, but most programming languages use `^` for XOR.

| A | B | A ⊕ B (Output) |
| - | - | -------------- |
| 0 | 0 | 0              |
| 0 | 1 | 1              |
| 1 | 0 | 1              |
| 1 | 1 | 0              |

For longer bit sequences, XOR is applied bit-by-bit, e.g., 0110 ⊕ 1010 = 1100.

XOR can be applied to integers by first converting them to binary. For strings, each character is converted to its Unicode integer code before XORing.

The challenge provides several hex-encoded XORed values involving three keys (KEY1, KEY2, KEY3) and an encrypted flag combined by XOR. Your goal is to use XOR’s properties to recover the original flag.

---

## Approach

XOR has four key properties relevant here:

* **Commutative:** A ⊕ B = B ⊕ A
* **Associative:** A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
* **Identity:** A ⊕ 0 = A
* **Self-Inverse:** A ⊕ A = 0

Using these, you can rearrange and simplify XOR expressions easily.

The encrypted flag is given as:

```
FLAG ⊕ KEY1 ⊕ KEY2 ⊕ KEY3
```

You are also given:

* `KEY2 ⊕ KEY1`
* `KEY3 ⊕ KEY2`
* `KEY1`

By rearranging, you can find each key by XORing these values accordingly. Once you find all three keys, XOR them together with the encrypted flag to recover the original flag.

---

## Tools
* Python
* `pwntools` library’s `xor()` function — handy for XOR operations on byte sequences.
* Hex to bytes conversion using `bytes.fromhex()`
* Knowledge of XOR properties to simplify expressions and solve for unknown keys.

---

## Code
```python
from pwn import xor

# Given hex strings decoded to bytes
key1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
key1_2 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")  # KEY2 ⊕ KEY1
key2_3 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")  # KEY3 ⊕ KEY2
flag_key123 = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")  # FLAG ⊕ KEY1 ⊕ KEY2 ⊕ KEY3

# Recover KEY2 by XORing KEY1 with KEY2 ⊕ KEY1
key2 = xor(key1, key1_2)

# Recover KEY3 by XORing KEY2 with KEY3 ⊕ KEY2
key3 = xor(key2, key2_3)

# XOR all keys together
combined_key = xor(key1, xor(key2, key3))

# Recover the flag by XORing the encrypted flag with all keys combined
flag = xor(flag_key123, combined_key)

# Print the decoded flag string
print(flag.decode())
```

---

### Output

```
crypto{x0r_i5_ass0c1at1v3}
```


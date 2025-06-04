
# 🧩 Working with Hex

**Source:** [CryptoHack - General](https://cryptohack.org/challenges/general/)

---

## 📝 Challenge Description

When we encrypt something, the resulting ciphertext often includes bytes that aren't printable ASCII characters. To make encrypted data more readable and portable, we often encode it in formats like **hexadecimal**.

Hex represents ASCII characters in base-16. First, each character is converted to its ASCII decimal value, then to hex. This challenge provides a flag encoded as a hex string. Decode it to reveal the flag.

```

63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d

````

---

## 🔧 Solution Code

```python
hex_data = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
flag = bytes.fromhex(hex_data).decode()
print(flag)
````

---

## 🏁 Flag

```
crypto{You_will_be_working_with_hex_strings_a_lot}
```

---


* `bytes.fromhex()` converts a hex string into its raw byte representation.
* `.decode()` converts the bytes to a readable ASCII/UTF-8 string.



# Bytes and Big Integers

**Source:** [CryptoHack - General](https://cryptohack.org/challenges/general/)

---

## 📝 Challenge Description

Cryptosystems like RSA operate on numbers, but plaintext messages are composed of characters. To bridge this gap, we convert messages into numbers using byte encoding.

For example:

* Message: `HELLO`
* ASCII bytes: `[72, 69, 76, 76, 79]`
* Hex: `0x48454c4c4f`
* Decimal: `310400273487`

We can reverse this process too, converting big integers back into messages using Python and the `long_to_bytes()` function from the PyCryptodome library.

---

## Approach

We are given a large decimal integer. It represents the hexadecimal form of a message that was originally encoded using byte values. Our goal is to reverse that and decode the original plaintext string.

---

## Tools

* Python
* PyCryptodome's `long_to_bytes()`
* Basic knowledge of ASCII and byte-level data representation

---

## Code

```python
from Crypto.Util.number import long_to_bytes

n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
message = long_to_bytes(n)
print(message.decode())
```

---

## Output

```
crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}
```

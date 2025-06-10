
# XOR Starter

**Source:** [CryptoHack - General](https://cryptohack.org/challenges/general/)

---

## Challenge Description

XOR (exclusive OR) is a fundamental bitwise operation used throughout cryptography. It returns:

* `0` if both bits are the same
* `1` if the bits are different

| A | B | A ⊕ B |
| - | - | ----- |
| 0 | 0 | 0     |
| 0 | 1 | 1     |
| 1 | 0 | 1     |
| 1 | 1 | 0     |

### String XOR

To XOR a string with a number:

1. Convert each character to its integer (`ord()` in Python)
2. XOR with the given number
3. Convert the result back to a character (`chr()` in Python)

In this challenge, you're given the string `"label"`.
You must XOR each character with the integer `13`, convert it back to a string, and wrap it as a flag:

```
crypto{new_string}
```

---

## Approach

* Loop through each character of the string `"label"`
* XOR each character's ASCII value with `13`
* Convert the XORed value back to a character
* Join the characters into a new string
* Wrap the result as the flag

This is a typical warm-up challenge to make sure you're comfortable with XOR operations in Python.

---

## Tools

* Python's built-in `ord()` and `chr()` for ASCII conversions
* Bitwise XOR: `^` operator
* String manipulation and list comprehensions

---

## Code

```python
def xor_str(text):
    return ''.join([chr(ord(c) ^ 13) for c in text])

original = "label"
result = xor_str(original)
print("crypto{" + result + "}")
```

---

## Output

```
crypto{aloha}
```

* XOR is reversible: `x ^ k ^ k = x`
* Useful in symmetric encryption schemes
* Python makes XOR manipulation very easy using `ord()` and `chr()`

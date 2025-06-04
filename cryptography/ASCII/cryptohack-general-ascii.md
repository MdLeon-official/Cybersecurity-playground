
**Source:** [CryptoHack - General](https://cryptohack.org/challenges/general/)

---

## 📝 Challenge Description

 ASCII is a 7-bit encoding standard which allows the representation of text using the integers 0-127.

Using the below integer array, convert the numbers to their corresponding ASCII characters to obtain a flag.

```

\[99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

````

---

## 🔧 Solution Code

```python
ascii_values = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
flag = ''.join([chr(i) for i in ascii_values])
print(flag)
````

---

## 🏁 Flag

```
crypto{ASCII_pr1nt4bl3}
```

---

* `chr()` converts an integer (0–127) into its corresponding ASCII character.
* Lists can be easily converted to strings using `''.join([...])`.

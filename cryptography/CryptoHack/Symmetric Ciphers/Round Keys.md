### **4. Round Keys**

```python
state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    result = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(s[i][j] ^ k[i][j])
        result.append(row)

    return result

def matrix2bytes(matrix):
    for i in range(4):
        for j in range(4):
            print(chr(matrix[i][j]), end="")


result = add_round_key(state, round_key)
matrix2bytes(result)
# FLAG: crypto{r0undk3y}
```

#### **Key Notes**

- **AES uses a 4×4 box** (called a matrix) to hold the message as bytes.

- In **AddRoundKey**, each byte of this box is **XORed** with a secret key (same size 4×4 box).

- This step is done **at the beginning** and **after every round** in AES.

- **XOR** is a special math trick — if you know the key, you can undo it easily.

- This step is the **only place where the key touches the message** — it makes AES secret and secure.

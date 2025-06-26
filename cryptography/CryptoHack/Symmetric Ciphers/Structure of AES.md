### **3. Structure of AES**

```python
def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    for i in range(4):
        for j in range(4):
            print(chr(matrix[i][j]), end="")


matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

# print(matrix2bytes(matrix))
matrix2bytes(matrix)

# FLAG: crypto{inmatrix}
```

* `chr()` converts an integer (0–127) into its corresponding ASCII character.

### **1. Quadratic Residues**

* Brute Force all the way.

```python
p = 29
ints = [14, 6, 11]

for a in range(1, p):
    z = pow(a, 2, p)
    if z in ints:
        print(f"{z} is a quadratic residue (a = {a})")
```

### Notes

* If $a^2 \mod p = x$, then $x$ is a **quadratic residue**
* Means: **you can get $x$** by squaring some number mod $p$
* If no such $a$, then $x$ is **not** a quadratic residue
* Always 2 roots: $a$ and $p - a$

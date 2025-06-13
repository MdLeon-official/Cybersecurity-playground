
# SSH Keys

**🔗 Source:** [https://cryptohack.org/challenges/general/](https://cryptohack.org/challenges/general/)

---

## Challenge Description

Find the subdomain of cryptohack.org which uses these parameters in its TLS certificate, and visit that subdomain to obtain the flag.

Challenge files:
  - transparency.pem

---

## Approach

The challenge requires us to extract the **modulus `n`** from an **SSH public key** file.

SSH public keys start with `ssh-rsa`, followed by a base64-encoded string. This string, once decoded, is structured using a binary format where each field is preceded by a 4-byte length. The three components inside the base64 blob are:

1. The algorithm name: `"ssh-rsa"`
2. The exponent `e`
3. The modulus `n` (which we want)

Each of these is stored as:

```
[4-byte length][data]
```

So, our task is to:

1. Decode the base64 part.
2. Skip over the algorithm and exponent.
3. Extract the modulus, and convert it to a decimal integer.

---

## Tools

* **Python**
* **Base64 decoding**
* **`struct` module** to unpack 4-byte lengths
* **Understanding SSH public key binary format**

---

## Code

```python
import base64
import struct

# Step 1: Read SSH public key and extract base64 part
with open("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub", "r") as f:
    b64 = f.read().strip().split()[1]  # Skip "ssh-rsa" and comment

# Step 2: Decode base64 string
raw = base64.b64decode(b64)

# Step 3: Skip the "ssh-rsa" part
l = struct.unpack(">I", raw[:4])[0]
raw = raw[4 + l:]

# Step 4: Skip the exponent (e)
l = struct.unpack(">I", raw[:4])[0]
raw = raw[4 + l:]

# Step 5: Extract the modulus (n)
l = struct.unpack(">I", raw[:4])[0]
modulus_bytes = raw[4:4 + l]

# Step 6: Convert to decimal
modulus = int.from_bytes(modulus_bytes, "big")
print(modulus)
```

---

## Output

```text
# Example output (yours will depend on the actual file)

```


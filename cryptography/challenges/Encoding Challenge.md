
# CryptoHack - Encoding Challenge

**Source:** [Encoding - CryptoHack](https://cryptohack.org/challenges/general/)
**Server:** `nc socket.cryptohack.org 13377`
**Files Provided:**

* `13377.py`: Server logic
* `pwntools_example.py`: Starter solution with [pwntools](https://docs.pwntools.com/en/stable/)

---

## Challenge Description

Now you've got the hang of the various encodings you'll be encountering, let's have a look at automating it.
Can you pass all 100 levels to get the flag?
The 13377.py file attached below is the source code for what's running on the server. The pwntools_example.py file provides the start of a solution.
For more information about connecting to interactive challenges, see the FAQ. Feel free to skip ahead to the cryptography if you aren't in the mood for a coding challenge!


---

## Approach / Thought Process

Each challenge round sends a JSON object with two keys:

* `"type"`: the encoding type (e.g., "base64")
* `"encoded"`: the encoded message

The script needs to:

1. Decode based on the type.
2. Send back the correct decoded string in the format: `{"decoded": "your_decoded_string"}`.

After 100 correct answers, the server responds with the final flag.

---

## Tools

* **[Pwntools](https://docs.pwntools.com/en/stable/)** for simple socket communication
* Python built-ins: `base64`, `codecs`, and standard decoding logic

---

## 🔧 Code / Implementation

```python
from pwn import *  # pip install pwntools
import json
import base64
import codecs

# Connect to the challenge server
r = remote('socket.cryptohack.org', 13377, level='debug')

# Receive JSON from server
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

# Send JSON to server
def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

# Loop through 100 encoding challenges
for i in range(100):
    received = json_recv()
    enc_type = received["type"]
    enc_data = received["encoded"]

    print(f"[{i+1}/100] Type: {enc_type}, Encoded: {enc_data}")

    if enc_type == "base64":
        decoded = base64.b64decode(enc_data).decode()
    elif enc_type == "rot13":
        decoded = codecs.decode(enc_data, 'rot_13')
    elif enc_type == "bigint":
        decoded = bytes.fromhex(enc_data.replace("0x", "")).decode()
    elif enc_type == "utf-8":
        decoded = ''.join([chr(b) for b in enc_data])
    elif enc_type == "hex":
        decoded = bytes.fromhex(enc_data.replace("0x", "")).decode()
    else:
        print("Unknown encoding type!")
        continue

    # Send the decoded message
    json_send({"decoded": decoded})

json_recv()
````

## Output

```
Flag: crypto{3nc0d3_d3c0d3_3nc0d3}
```



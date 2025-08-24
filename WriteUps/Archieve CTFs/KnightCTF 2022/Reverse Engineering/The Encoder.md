### The Encoder

Download the challenge file. Make that executabe: **`chmod +x the_encoder.out`**

Ran the encoder to see how it maps characters to numbers. I found this:

* `A–Z → 1402–1427`
* `a–z → 1434–1459`
* `0–9 → 1385–1394`
* `_ → 1432`, space → `1369`, `{ → 1460`, `} → 1462`


Then I wrote a Python script to reverse the process using the offsets.

```python
nums = [1412, 1404, 1421, 1407, 1460, 1452, 1386, 1414, 1449, 1445, 
        1388, 1432, 1388, 1415, 1436, 1385, 1405, 1388, 1451, 1432, 
        1386, 1388, 1388, 1392, 1462]

flag = ""
for n in nums:
    if 1402 <= n <= 1427:
        flag += chr((n - 1402) + ord('A'))
    elif 1434 <= n <= 1459:
        flag += chr((n - 1434) + ord('a'))
    elif 1385 <= n <= 1394:
        flag += chr((n - 1385) + ord('0'))
    elif n == 1369:
        flag += " "
    elif n == 1432:
        flag += "_"
    elif n == 1460:
        flag += "{"
    elif n == 1462:
        flag += "}"

print("Flag:", flag)
```

It gives the flag.

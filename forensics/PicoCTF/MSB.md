## [MSB](https://play.picoctf.org/practice/challenge/359?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded the image.

2. Installed Pillow:

   ```bash
   pip install Pillow
   ```
3. Downloaded the script:

   ```bash
   wget https://raw.githubusercontent.com/Pulho/sigBits/master/sigBits.py
   ```
4. Ran the script to extract MSB data:

   ```bash
   python3 sigBits.py -t=msb Ninja-and-Prince-Genji-Ukiyoe-Utagawa-Kunisada.flag.png
   ```
5. Searched the output:

   ```bash
   grep -o -E "picoCTF.{0,50}" outputSB.txt
   ```

#### 🏁 Flag:

```
picoCTF{xxxxxxxxxxxxxxxxxxxxxxxxxxxx}
```

#### Key Notes:

* MSB steganography hides data in the **most significant bits** of pixel color values.
* `sigBits.py` is a Python tool that extracts data from LSB or MSB.
* Use `grep` with regex to extract flags from noisy output.

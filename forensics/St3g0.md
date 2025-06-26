## [St3g0](https://play.picoctf.org/practice/challenge/305?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded the provided file: `pico.flag.png`
2. Used the tool `zsteg` to analyze the image:

   ```bash
   zsteg pico.flag.png
   ```
3. The flag was revealed in one of the LSB channels.

#### 🏁 Flag:

```
picoCTF{7h3r3_15_n0_5p00n_a9a181eb}
```

#### Key Notes:

* `zsteg` is a steganography analysis tool specialized for PNG/BMP.
* It scans **Least Significant Bits (LSBs)** in color channels for hidden data.
* Useful for **CTF stego challenges** where data is subtly embedded in images.

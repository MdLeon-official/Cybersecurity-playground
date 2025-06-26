## [hideme](https://play.picoctf.org/practice/challenge/350?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded the provided challenge file.
2. Ran the `strings` command to look for readable text:

   ```bash
   strings <file> | less
   ```

   Found this interesting string:

   ```
   secret/UT
   secret/flag.pngUT
   ```
3. This indicated that an image named `flag.png` might be hidden inside.
4. Extracted hidden files using:

   ```bash
   binwalk -e <file>
   ```
5. A new folder was created, inside which was a `secret/flag.png` image.
6. Opened the image and uploaded it to [ImageToText](https://www.imagetotext.info/) to extract the text from the image, which revealed the flag.

#### 🏁 Flag:

```
picoCTF{Hiddinng_An_imag3_within_@n_ima9e_dc2ab58f}
```

#### Key Notes:

* `strings` helps find readable ASCII/Unicode strings in binary files — good for hints.
* `binwalk -e` is used to extract embedded files (like images) from a binary.

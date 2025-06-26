## [Mob psycho](https://play.picoctf.org/practice/challenge/420?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded and extracted the APK.

2. Searched for flag:

   ```bash
   strings * | grep flag
   ```

   → Found: `res/color/flag.txt`

3. Go to `res/color/`.

4. Printed contents:

   ```bash
   cat res/color/flag.txt
   ```

5. Decoded the hex using:

   ```bash
   cat res/color/flag.txt
   ```

6. Then go to cyberchef or any other platform and decode the hex.

#### 🏁 Flag:

```
picoCTF{ax8mC0RU6ve_***********_a3e...}
```

#### Key Notes:

* APKs can be unzipped like regular zip files.
* Use `strings` + `grep` to quickly scan large file sets for flag clues.
* Use `xxd -r -p` to decode hex-encoded strings.
* `ls -R`: Recursively list all files and directories

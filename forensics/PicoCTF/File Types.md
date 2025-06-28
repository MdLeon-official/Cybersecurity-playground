### [File Types](https://play.picoctf.org/practice/challenge/268?category=4&page=3)


### 🧪 Steps to Solve:

1. **Downloaded the file**:
   The given file was named `Flag.pdf`, but it was **not** a real PDF.

2. **Renamed the file to .tar for clarity** (optional but helpful):

   ```bash
   mv Flag.pdf Flag.shar
   ```

3. **Found a shar archive inside**. Checked it using `less` or `file`:

   ```bash
   less Flag.shar
   ```

4. **Unpacked the shar archive** using `unshar`:

   ```bash
   unshar Flag.shar
   ```

5. A file named `flag` appeared. Checked its file type:

   ```bash
   file flag
   # Output: current ar archive
   ```

6. **Extracted it using `ar`**:

   ```bash
   ar x flag
   ```

7. Tried to execute it but failed (it's not a binary):

   ```bash
   ./flag  # => Exec format error
   ```

8. Ran `binwalk` to identify its compression type:

   ```bash
   binwalk flag
   # Found bzip2 compression
   ```

9. Extracted using `binwalk -e`:

   ```bash
   binwalk -e flag
   ```

10. Moved into the extracted folder and found file `20`, checked it:

```bash
file 20
# Output: gzip compressed data
```

11. Ran `binwalk -e 20` again:

```bash
binwalk -e 20
```

12. Inside `_20.extracted/`, found `flag.gz`, extracted it:

```bash
gzip -d flag.gz
```

13. Found a `flag` file again, checked it:

```bash
file flag
# Output: lzip compressed data
```

14. Decompressed it:

```bash
lzip -d flag
```

15. Found `flag.out`, checked again:

```bash
file flag.out
# Output: LZ4 compressed data
```

16. Renamed and decompressed:

```bash
mv flag.out flag.lz4
lz4 -d flag.lz4
```

17. Got a new `flag`, checked:

```bash
file flag
# Output: LZMA compressed data
```

18. Renamed and decompressed:

```bash
mv flag flag.lzma
lzma -d flag.lzma
```

19. Got another `flag`, checked:

```bash
file flag
# Output: lzop compressed data
```

20. Renamed and decompressed:

```bash
mv flag flag.lzop
lzop -d flag.lzop
```

21. Got yet another `flag`, checked:

```bash
file flag
# Output: lzip compressed data
```

22. Decompressed:

```bash
lzip -d flag
```

23. Got `flag.lzip.out`, checked:

```bash
file flag.lzip.out
# Output: XZ compressed data
```

24. Extracted using `binwalk -e`:

```bash
binwalk -e flag.lzip.out
```

25. Inside the final extracted folder, found a file `0` that contains a **hex-encoded flag**:

```bash
cat 0
```

26. Decoded hex using:

```bash
hex -d 0
```

---

### 🏁 Flag:

```
picoCTF{f1len@m3_m@n1pul@t10n_f0r_*********_3c79c5ba}
```

---

### Key Notes:

* Always inspect unknown file types using `file` and `binwalk`.
* Each layer may use a different compression: `.bz2`, `.gz`, `.lzip`, `.lzma`, `.lzop`, `.xz`.
* Use appropriate decompressors:

  * `gzip`, `lzip`, `lzma`, `lz4`, `lzop`, `xz`, `binwalk`
* Hex data can be decoded using:

  ```bash
  hex -d 0
  ```

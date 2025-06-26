## [Dear Diary](https://play.picoctf.org/practice/challenge/413?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded the `disk.flag.img.gz` file from the challenge.
2. Decompressed it using:

   ```bash
   gzip -d disk.flag.img.gz
   ```
3. Opened **Autopsy** (a digital forensics GUI tool).
4. In Autopsy, followed these steps:

   ```
   New Case → Add Case Name → Next → Add Host → Enter Host Name → Next
   → Add Image File → Browse to decompressed .img file → Next → Finish
   ```
5. In the **ANALYZE** tab, selected **Keyword Search**, searched for `.txt`, and found several text files.
6. Each `.txt` file contained a part of the flag.
7. Combined all pieces to form the complete flag.

#### 🏁 Flag:

```
picoCTF{1_533_n4m35_80d24b30}
```

#### Key Notes:

* `.img` files are disk images — treat them like virtual hard drives.
* **Autopsy** is a powerful forensic tool to analyze disk images, recover files, search keywords, etc.
* Keyword search helps you quickly locate interesting file types (like `.txt`, `.jpg`, etc.).
* Sometimes flags are split into multiple files — piece them together carefully.

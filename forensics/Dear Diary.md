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

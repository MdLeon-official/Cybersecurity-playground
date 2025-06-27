### 1. [Operation Oni](https://play.picoctf.org/practice/challenge/284?category=4&page=1)

#### 🧪 Steps to Solve:

1. Downloaded and decompressed the file:

```bash
gzip -d disk.img.gz
```

2. Identified partitions:

```bash
mmls disk.img
```

3. Found multiple partitions — selected the second Linux one (0x83).
4. Listed files and directories:

```bash
fls -r -o <partition_offset> disk.img
```

5. Navigated through directories using `fls` — found `.ssh` folder.
6. Located private key file (likely `id_rsa` or similar).
7. Extracted key with:

```bash
icat -o <partition_offset> disk.img <inode> > id_rsa
```

8. Fixed permissions:

```bash
chmod 600 id_rsa
```

9. Logged into SSH:

```bash
ssh -i id_rsa -p <port> <username>@<ip>
```

10. After login, found the flag in home directory.

#### 🏁 Flag:

```
picoCTF{k3y_5l3u7h_339601ed}
```

#### Key Notes:

* Use `mmls` to find partitions and their offsets.
* Use `fls` and `icat` from SleuthKit to locate and extract hidden files.
* SSH keys need `chmod 600` permission to be accepted.
* Login with SSH private key using `ssh -i`.

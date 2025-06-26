## [Torrent Analyze](https://play.picoctf.org/practice/challenge/311?category=4&page=2)

#### 🧪 Steps to Solve:

1. Downloaded the pcap file.

2. Opened it with Wireshark:

```bash
wireshark torrent.pcap
```

3. Applied display filter:

```
bt-dht
```

4. Found many `info_hash` fields in the packets.
5. Right-clicked an `info_hash` → *"Apply as Column"*.
6. Sorted the new column to find the most frequent hash.
7. Searched the most common hash on Google.
8. Found it matched a Linux `.iso` file on Linuxtracker.
9. Used filename as flag.

#### 🏁 Flag:

```
picoCTF{ubuntu-19.10-desktop-amd64.iso}
```

#### Key Notes:

* Use `bt-dht` filter to view BitTorrent traffic.
* `info_hash` identifies the file being downloaded.
* Most frequent hash often leads to the actual file.

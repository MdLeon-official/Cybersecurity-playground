[Eavesdrop](https://play.picoctf.org/practice/challenge/264?category=4&page=3)


## Steps

1. **Download File**  
   - Get `capture.flag.pcap`.

2. **Open in Wireshark**  
   - Run `wireshark capture.flag.pcap`.  
   - Filter TCP traffic, right-click a packet, select `Follow -> TCP Stream`.  
   - Find clue: `openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123` and port `9002`.

3. **Check Port 9002**  
   - Filter `tcp.port == 9002`, follow TCP stream, switch to `Show As RAW`.  
   - See : `53616c7465645f5f3c4b26e8b8f91e2c4af8031cfaf5f8f16fd40c25d40314e6497b39375808aba186f48da42eefa895`.  
   - Save as `file.des3`.

4. **Decrypt File**  
   - Run: `openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123`.  
   - Creates `file.txt`.

5. **Get Flag**  
   - Run `cat file.txt`.  
   - Flag: `picoCTF{nc_73115_411_0ee7267a}`.

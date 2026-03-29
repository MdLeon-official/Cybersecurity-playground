# Lab: JWT authentication bypass via unverified signature

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)

First, log in with the provided credentials: `wiener:peter`.  
Once logged in, try to access `/admin`. You’ll see a message saying:  
> Admin interface only available if logged in as an administrator.

Now, try accessing `/admin` again, but this time intercept the request in Burp Suite. You’ll notice a JWT token in the request. It looks something like this:
```
eyJraWQiOiI1ZGQ1NTBmZC0yYzE3LTQ5MGYtOWY0YS0wZWE0NTIwMWVmY2YiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc3NDUyOTEyNCwic3ViIjoid2llbmVyIn0.hsU98XxkwqOG8ILIvaox1f_9w-XuGP5GzRNp2Ah_K6v3YT9Y7sTDcUt9aYJY8sFDedtvkhN7uMLNjmyLN9rgkmzRzBXxIPaMQgeOU5QDHSEiZAOeTOfuNdj0nc55XeS150bcjfMX1xDtG_yJ-bsC31Zhwj3VRUc6EE5USAL27WJsSW6wW8CQu-x_IoDFvL5sLJZQltIXxirx7Nr7Xa45qVvUHARWzhqJlzwIH4AXmvi1wnJoqt5Vw6Bs5p3925rmYJ2IXEA0Q3YPYCwa7G9gxmuj4QXcxl1iRb6qSscXUOw9F9PbraRtnxKwAJDm-pD_VMigxgN8JFlghGbNVqLfiw
```
Head over to [jwt.io](https://jwt.io/) and paste the token to decode it.  You’ll see the payload looks like this:
```
{
  "iss": "portswigger",
  "exp": 1774529124,
  "sub": "wiener"
}
```
Since the lab is about unverified signatures, the server isn’t actually checking the signature, so we can modify the token without worrying about signing it. Change the `"sub"` field from `"wiener"` to `"administrator"`, then copy the newly encoded token from jwt.io. Back in Burp, replace the original token in the request with this modified one and forward the request.  
Now you should have access to the admin panel.
You’ll see an option to delete user `carlos`. Click it - but if you just click it from the browser, you might still get the “admin only” message because the browser is using the old token in the background.  
So intercept the delete request in Burp, replace the token there with the same modified `administrator` token, and forward it.
This time, the request goes through and Carlos is deleted. The lab solves.



# Lab: JWT authentication bypass via flawed signature verification

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)

Start by logging in with the provided credentials: `wiener:peter`.  
Then try to access `/admin` – you’ll see the message:  
> Admin interface only available if logged in as an administrator.

Now intercept the request to `/admin` again in Burp Suite. You’ll see a JWT token in the request. Copy the token and decode it using a tool like [jwt.io](https://jwt.io/).  
The decoded payload looks like:

```json
{
  "kid": "23045a4a-d9eb-4918-9e4d-7cc274861a0c",
  "alg": "RS256"
}

{
  "iss": "portswigger",
  "exp": 1774529124,
  "sub": "wiener"
}
```

In this lab, the server doesn’t properly verify the signature - it even accepts tokens with the `"alg": "none"` header. So we can forge a token that claims we are an administrator without needing a signature.

Modify the token in jwt.io:
- Change the **header** from `"alg": "RS256"` to `"alg": "none"`.
- In the **payload**, change `"sub": "wiener"` to `"sub": "administrator"`.

Jwt.io will generate a new token that looks like:

```
eyJraWQiOiIyMzA0NWE0YS1kOWViLTQ5MTgtOWU0ZC03Y2MyNzQ4NjFhMGMiLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc3NDU1NjI0NSwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.
```

Notice there’s no signature part at the end.

Now go back to Burp, replace the original token in the intercepted request with this new one, and forward the request.  
You should now have access to the admin panel.

In the admin panel, you’ll see a button to delete user `carlos`. If you click it directly, the browser will use the old token, so you’ll get the same “admin only” message. Instead, intercept the DELETE request in Burp, replace the token there with your forged `none` token again, and forward it.

The request goes through, Carlos is deleted, and the lab is solved.


# Lab: JWT authentication bypass via weak signing key

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key)

First, log in with the credentials `wiener:peter`. Then try to access `/admin` – you’ll see the usual message:  
> Admin interface only available if logged in as an administrator.

Now intercept the request to `/admin` in Burp Suite. Look at the JWT token - it’s a bit different from the previous lab. If you decode it at [jwt.io](https://jwt.io/), you’ll see the header uses `"alg": "HS256"` (symmetric signing) and the payload contains `"sub": "wiener"`.

Because the server uses a weak symmetric key, we can brute‑force it to then forge a valid token.  

I used `hashcat` with the mode for JWT (mode 16500) and a wordlist of common secrets. The command looked like this:

```bash
hashcat -a 0 -m 16500 "eyJraWQiOiI0ZjkyNDRjMy05NDMzLTQ4YTItYTI0Yi0zM2E3MGZlM2IzOGMiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc3NDYxMTI3NSwic3ViIjoid2llbmVyIn0.n7yxGfEWiM4m2F7Zv1N5KeMLkSqs3xl4Tk2LvBpE7tY" /usr/share/wordlists/jwt.secrets.list
```

Hashcat quickly cracked it, revealing the secret: `secret1`.

Now that I had the signing key, I went back to jwt.io. I pasted the original token, changed the `sub` field from `"wiener"` to `"administrator"`, and then – importantly – signed the new token using the secret `secret1` with the HS256 algorithm. This gave me a valid JWT claiming I was an administrator.

In Burp, I replaced the token in the intercepted `/admin` request with this newly signed token and forwarded it. I was then able to access the admin panel.

Finally, I clicked the button to delete user `carlos`. The browser’s initial request used the old token, so I intercepted the DELETE request, swapped in my forged token again, and forwarded it. This time the deletion succeeded, and the lab was solved.



# Lab: JWT authentication bypass via jwk header injection

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection)

After logging in with `wiener:peter` and trying to access `/admin`, I saw the usual “admin only” message. Intercepting the request in Burp, I noticed the JWT was signed with an RSA algorithm. The twist in this lab is that the server is configured to accept a `jwk` (JSON Web Key) header parameter - meaning if we can embed our own public key and sign the token with the corresponding private key, the server will trust it.

I used Burp’s JWT Editor extension (available from the BApp store) to make this easy. First, I opened the JWT Editor Keys tab in Burp’s main tab bar. I clicked “New RSA Key” and then “Generate” to create a fresh RSA key pair (no need to worry about key size, the extension handles it).

Then I went back to the intercepted `GET /admin` request and switched to the JSON Web Token tab (also added by the extension). I edited the payload, changing the `sub` claim from `"wiener"` to `"administrator"`.

At the bottom of that tab, I clicked “Attack” and chose “Embedded JWK”. A dialog popped up asking which key to use - I selected my newly generated RSA key. Burp automatically added a `jwk` header to the JWT containing my public key, signed the whole token with my private key, and updated the request.

I forwarded the request and was immediately granted access to the admin panel.

Finally, I clicked the button to delete user `carlos`. The browser’s request used the original token, so I intercepted that DELETE request, again switched to the JSON Web Token tab, repeated the “Embedded JWK” attack with my key, and forwarded it. This time the deletion succeeded, and the lab was solved.



# Lab: JWT authentication bypass via jku header injection

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jku-header-injection)

After logging in as `wiener:peter`, I tried to access `/admin` and got the usual “admin only” message. Intercepting the request in Burp, I saw the JWT was signed with RSA. In this lab, the server trusts the `jku` (JSON Key URL) header, which points to a location containing the public key used to verify the signature. If I can host my own JWK Set and make the token point to it, I can sign the token with my matching private key and impersonate an administrator.

I used Burp’s JWT Editor extension again. First, I went to the **JWT Editor Keys** tab and generated a new RSA key pair (simply click “New RSA Key” and then “Generate”). This gave me a private key I could use to sign tokens, and a corresponding public key that I’d need to serve.

Next, I opened the exploit server that comes with the lab. In the **Body** section, I created a minimal JWK Set - an empty JSON object with a `keys` array. Then I went back to the JWT Editor Keys tab, right‑clicked my generated RSA key, and selected **Copy Public Key as JWK**. I pasted that JSON object into the `keys` array on the exploit server, so the final JWK Set looked something like:

```json
{
  "keys": [
    {
      "kty": "RSA",
      "e": "AQAB",
      "kid": "a23c8c7b-6b2c-4b7a-8bc4-27265fd398cf",
      "n": "yyEg9XAxJBTb1Fmikl66ZCbXUMbqPd0taLVr0So5EEkrJPWc47ZMQVRAX-x_2O3EbUlGFnX_ka-Ul3aGPXSS1IrbUaJTERkP9S2avr-hNbwRF41MzotXx8R704WThjlINugp62QLrY2xwnd2Jg0TjqWCKiN7KEKGFDInbr2PmOy5rn2bRBTHxjN9kel6GqzG3_7uQ__1akIyMnZN1PHgMJpxjly5aQs4TbJIHI5k6Bk3C4zbgtCOWHz9AsqYAnTM4PrFrGolt5FzP_-6XaKv9g4EXyieOTuvMmzU63X34x-6_ozde3GtK8GTvJt9x9mBuIQaP9EQA7S_Lx0SWw2Ptw"
    }
  ]
}
```

I stored the exploit, noting the URL (e.g., `(https://exploit-0ad4008d0446************ed004c.exploit-server.net/.well-known/jwks.json)`).

Now I went back to Burp Repeater and the intercepted `GET /admin` request. I switched to the JSON Web Token tab and modified the JWT:

- In the header, I replaced the existing `kid` (key ID) with the `kid` from my JWK Set (a23c8c7b-6b2c-4b7a-8bc4-27265fd398cf - the one I pasted on the exploit server).
- I added a new `jku` header parameter, setting its value to the URL of my JWK Set (the exploit server URL).
- In the payload, I changed the `sub` claim from `"wiener"` to `"administrator"`.
```json
{
    "kid": "a23c8c7b-6b2c-4b7a-8bc4-27265fd398cf",
    "jku": "https://exploit-0ad4008d0446fb9b801e89bc01ed004c.exploit-server.net/.well-known/jwks.json",
    "alg": "RS256"
}
```

Finally, I clicked **Sign** at the bottom, selected my RSA key, and made sure **Don't modify header** was selected (so the `jku` and `kid` I manually set stayed intact). The extension signed the token with my private key.

I sent the request and - success! I was granted access to the admin panel. In the response, I found the link to delete user `carlos`: `/admin/delete?username=carlos`. I sent a request to that endpoint (intercepting again to ensure the same forged token was used) and the lab was solved.



# Lab: JWT authentication bypass via kid header path traversal

[LINK](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal)

After logging in with `wiener:peter` and trying to access `/admin`, I saw the familiar “admin only” message. Intercepting the request in Burp, I examined the JWT. The header looked like this:

```json
{
  "kid": "36452a4a-d9eb-4918-9e4d-7cc274861a0c",
  "alg": "HS256"
}
```

In this lab, the server uses the `kid` (key ID) parameter to construct a file path to retrieve the symmetric signing key. Because the server doesn’t properly sanitize the `kid`, I could use directory traversal to point it to a predictable file on the server - in this case, `/dev/null`, which is an empty file.

I used Burp’s JWT Editor extension to modify the token. I changed the header to:

```json
{
  "kid": "../../../dev/null",
  "alg": "HS256"
}
```

Since `HS256` is a symmetric algorithm, the signing key would be whatever the server reads from the file. `/dev/null` is empty, so effectively the key becomes an empty string.

In the payload, I changed the `sub` claim from `"wiener"` to `"administrator"`:

```json
{
  "iss": "portswigger",
  "exp": 1774700851,
  "sub": "administrator"
}
```

Now I needed to sign the token with an empty key. The JWT Editor extension has a convenient option for this: after modifying the token, I clicked **Attack** and selected **Sign with empty key**. The extension signed the token using an empty string as the secret, matching what the server would derive from `/dev/null`.

I sent the request and was immediately granted access to the admin panel. In the response, I found the link to delete user `carlos` at `/admin/delete?username=carlos`. I intercepted that DELETE request, replaced the token with my forged one (again using the empty key signature), and forwarded it. The user was deleted, and the lab was solved.


# Lab: JWT authentication bypass via algorithm confusion

After logging in as `wiener:peter` and trying to access `/admin`, I got the familiar “admin only” message. Intercepting the request in Burp, I saw the JWT was signed with `RS256` (asymmetric RSA). The twist here is that the server is vulnerable to **algorithm confusion** - it accepts `HS256` (symmetric HMAC) tokens but uses the same verification logic. If I can obtain the server’s public RSA key and then sign a token using `HS256` with that public key as the HMAC secret, the server will verify it successfully, effectively letting me forge any token .

First I needed to find the public key. I checked a few common endpoints:

- `/.well-known/jwks.json`
- `/jwks.json`
- `/auth/jwks`
- `/api/jwks`
- `/keys`
- `/security/jwks`
- `/public-keys`

Bingo – `/jwks.json` returned a valid JWK Set:

```json
{"keys":[{"kty":"RSA","e":"AQAB","use":"sig","kid":"0524f4c1-e32a-47bb-9fc5-4f4cac5328ae","alg":"RS256","n":"o94tLBv6Avt97VYOoN8XmxVGW40xZlAabXmIvUxIU67G4fh8Aj1AuvUFvfwZAde7HAzGtIii3HNw7e9DuYdMhhBya5AZc0wjxXCjvWoujf54i_qqDnnvM7RQTOdLMgFA8qoVCIGwVCPM_GS7Oda6YpkIAJMo7xm69A2-WIQrTuabSKVl1NFVSPANfU9OcSb60D9zq0SHDC6NlKO_73Rlz5-TSPJOrt0ubiN4BtNc_Q2lJbbrF3K98xD37iQQARZ8BgvAXXp43lalwYuc1EDL5O_NfQM-LiXnfk4rpv28A8rBNPvtwu8NTZ5IMXTXLAfaNaQan6b6sEeefQHHO6cTbw"}]}
```

The lab description said the server stores its public key as an X.509 PEM file . So I needed to convert this JWK into a PEM, then into a Base64‑encoded string that I could use as a symmetric key.

Using Burp’s JWT Editor extension:

- I went to **JWT Editor Keys** → **New RSA Key** → selected the **PEM** format option.
- I pasted the entire JWK object into the dialog. The extension automatically parsed it and displayed the RSA public key.
- Then I right‑clicked the key and selected **Copy Public Key as PEM**.
- I opened Burp’s **Decoder** tab, pasted the PEM, and encoded it as **Base64**. This is the value that will become the `k` parameter of our symmetric key.

Now, here’s where the **real‑world nuance** comes in. In a perfect world, copying the PEM and Base64‑encoding it just works. But in reality, **tiny formatting differences can break the attack** . Things like:

- Extra spaces or tabs inside the key
- Newline characters at the beginning or end of the PEM
- Different line break styles (LF vs CRLF)
- Whether the Base64 padding (`=`) is included or stripped
- Whether the tool you’re using expects raw bytes or a string

To be safe, after pasting the PEM into the Decoder, I made sure there was a newline at the end of the file (some servers are picky about that). I also tested without the newline, and with different whitespace - in real engagements you might need to brute‑force these tiny variations.

Once I had the Base64‑encoded PEM, I went back to **JWT Editor Keys** and clicked **New Symmetric Key**. I left the generated `k` value as a placeholder, then replaced it with my Base64 string. This created a symmetric key whose `k` value is *exactly* the server’s public RSA key in PEM format, Base64‑encoded.

Now the actual attack:

- In Repeater, I switched to the **JSON Web Token** tab.
- I changed the `alg` header from `RS256` to `HS256`.
- In the payload, I set `"sub": "administrator"`.
- I clicked **Sign**, selected my newly created symmetric key, and made sure **Update/generatea "alg" parameter** was checked (so my `HS256` stayed).
- The extension signed the token using HMAC‑SHA256 with the public key as the secret.

I sent the request and - success! I was granted access to the admin panel. In the response, I found the delete endpoint for `carlos`: `/admin/delete?username=carlos`. I sent that request (replacing the token again with my forged one) and the lab was solved.

# Lab: JWT authentication bypass via algorithm confusion with no exposed key

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

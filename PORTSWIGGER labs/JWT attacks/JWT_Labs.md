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

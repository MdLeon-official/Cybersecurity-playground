# Admin has the power


1. Open the webpage and inspect the source code.
2. In the HTML comments, find the maintenance credentials:

   ```
   user: support  
   password: x34245323
   ```
3. Log in using these credentials.
4. Open Burp Suite and intercept the login request.
5. Send the request to the Repeater tab.
6. In the request body or parameters, You will find `role=support`.
7. Change `role` value from `support` to `admin`.
8. Send the modified request.
9. The response will contain the flag.



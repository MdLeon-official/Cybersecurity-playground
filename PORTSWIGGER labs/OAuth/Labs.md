# Authentication bypass via OAuth implicit flow

Login using given credentials -> capture those request in burp -> In /authenticate endpoint see three parameter used:
```
{"email":"wiener@hotdog.com","username":"wiener","token":"Vn4FQ4XCEOS8cw60khEh8w1c21q7rzrSpW3rS7pS8ok"}
```
Change the username to carlos and email to given carlos email -> send -> see the request in browser -> solved




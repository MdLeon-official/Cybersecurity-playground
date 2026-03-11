# [Neighbour](https://tryhackme.com/room/neighbour)


This is just a basic idor problem
First view page source of that website, there you will get the login credentials:
```
            <!-- use guest:guest credentials until registration is fixed. "admin" user account is off limits!!!!! -->
```
Login using that credential. After login look at the url, you will see something like `user=guest`
So make that `user=admin` and enter.
You'll get the flag.

# Lab: Reflected XSS into HTML context with nothing encoded - [Click](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
To solve the lab, perform a cross-site scripting attack that calls the alert function.

So you just need to use this cookie in the search bar:
```
<script>alert(1)</script>
```

Lab Solved.

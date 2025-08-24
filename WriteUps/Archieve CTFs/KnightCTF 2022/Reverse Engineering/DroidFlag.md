### Droid Flag

I started by decompiling the APK using `apktool`:

```bash
apktool d DroidFlag.apk
```

Then, I checked `MainActivity.smali` ((DroidFlag/smali/org/knightsquad/droidflag) and saw that it creates a `StringHandler` instance. After decompiling `StringHandler.smali` to Java, I found that it has four methods:

* `getS1()` returns the string `s5` from resources.
* `getS2()`, `getS3()`, and `getS4()` return strings `s6`, `s7`, `s8` from resources **in reversed order**.

Next, I looked at `DroidFlag/res/values/strings.xml` and found the relevant strings:

```xml
<string name="s5">****</string>
<string name="s6">******</string>
<string name="s7">******</string>
<string name="s8">******</string>
```

Since `s6`, `s7`, and `s8` were reversed, I used a simple Python script to reverse them and combine all parts into the real flag:

```python
s5 = "****"
s6 = "******"
s7 = "******"
s8 = "******"
flag = s5 + s7[::-1] + "_" + s6[::-1] + "_" + s8[::-1] + "}"
print(flag)
```
This gave me the actual flag.


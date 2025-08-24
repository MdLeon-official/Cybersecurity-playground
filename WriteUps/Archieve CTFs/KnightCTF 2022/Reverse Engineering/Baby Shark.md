

### Babyshark

I started by extracting the contents of the `babyshark.jar` file with:

```bash
jar -xvf babyshark.jar
```

Inside the `kctf/constants/` directory I found a file called `Strings.class`. I ran it through an online Java decompiler and got a `Strings.java` file.

Looking at the decompiled code, I saw several Base64-encoded strings. The last one, `_0xflag`, stood out. After decoding it, I got the final flag:

```
KCTF{*****************?}
```


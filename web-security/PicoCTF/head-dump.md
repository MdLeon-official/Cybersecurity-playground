## [head-dump](https://play.picoctf.org/practice/challenge/476?category=1&page=1)

#### 🧪 Steps to Solve:

1. Explored site, found /api-docs via API article.
2. Identified /heapdump endpoint in Swagger.
3. Executed it, got a .heapsnapshot file.
4. Used grep to find the flag inside the dump.
   ```bash
   cat heapdump-1750184619426.heapsnapshot | grep pico
   ```

#### 🏁 Flag:

```
picoCTF{Pat!3nt_15_Th3_K3y_ad7ea5ae}
```



# Milkslap - [Click](https://play.picoctf.org/practice/challenge/139?category=4&page=4&search=)



### Steps to Solve:

1. Noticed there’s no direct file to download, but clicking the **image** in the description opens the **actual PNG file**.
2. Downloaded the PNG using:

   ```bash
   wget http://mercury.picoctf.net:48380/concat_v.png
   ```
4. Since it’s a PNG and has animation, suspected **steganography**.
5. Used:

   ```bash
   gem install zsteg
   zsteg concat_v.png
   ```
6. Found the flag hidden in image data.


### Flag:

```
picoCTF{imag3_m4n1pul4t10n_*****}
```



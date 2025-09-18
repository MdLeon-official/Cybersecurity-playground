Open the file in Ghidra.

```
  if (local_40 == 0x539) {
    iVar1 = strcmp(local_38,"Sup3rS3cr3tP455W0rd\n");
    if (iVar1 == 0) {
      puts("Correct!\nHere is your flag\n");
      for (local_3c = 0; local_3c < 0x1b; local_3c = local_3c + 1) {
        putchar((int)(char)((char)local_3c + 0x69U ^
                           (byte)*(undefined4 *)(flag + (long)(int)local_3c * 4)));
      }
    }
    else {
      puts("Wrong password!");
    }
  }
```


Heres The password is `Sup3rS3cr3tP455W0rd` and the secret code is `1337`.

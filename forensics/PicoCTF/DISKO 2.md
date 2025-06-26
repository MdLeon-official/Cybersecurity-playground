## [DISKO 2](https://play.picoctf.org/practice/challenge/506?category=4&page=1)

#### 🧪 Steps to Solve:
1. Downloaded the `disko-2.dd` file from the challenge.

2. First used the strings command:
```bash
   strings disko-2.dd | grep pico
   ``` 
But there was too many flags (You can brute force your way through)

3. Then used this command to see different partitions of the disk
```bash
   mmls disko-2.dd
   ```

4. Then I used the ```dd``` command to extract the linux partition(why the linux partition? - There was this hint "The right one is Linux!")
```bash
   dd if=disko-2.dd of=LinxPartition.img bs=512 skip=2048 count=51200
   ```
Here, if=main .dd file
      of=Name of the extracted file
      bs=Units are in 512-byte sectors(use mmls)
      skip=start of the selected partition
      count=Basically length of the selected partition
      
5. Then used ```strings``` command
```bash
   strings LinxPartition.img | grep pico
   ```


#### 🏁 Flag:

```
picoCTF{4_P4Rt_1t_i5_a93c3ba0}
```

#### Key Notes:
- *Use mmls to identify partition layout in .dd images.*
- *dd is powerful for carving specific file systems out of images.*
- *strings + grep helps quickly find flags in raw files.*

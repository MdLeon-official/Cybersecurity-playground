# Corrupted File 

First see the file header: `xxd -l 6 unopenable.gif`

We will see that the file header of the file is not correct.

So We just need to change the file header. To change the file header use: `printf "GIF89a" | cat - unopenable.gif > fixed.gif`

Now view the gif file. But the gif file is running too fast. 

`convert fixed.gif one.jpg` (This will convert the gif file to many image file). Now you will find some base64 code. Combine them
and decode. You'll get the flag.

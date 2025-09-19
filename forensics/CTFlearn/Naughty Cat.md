# Naughty Cat 

Download the challenge file (cut3_c4t.png). Use `binwalk -e cut3_c4t.png` to extract the hidden files. 
Go to the extracted folder. Theres a corrupted .rar file. So to make this file okay we can use `hexedit y0u_4r3_cl0s3.rar`
Change the hex to `52 61 72 21 1A 07 01 00`. After changing decompressed the file using `unrar x y0u_4r3_cl0s3.rar`. Now it
wants a password. So to get the password I used audacity to play the audio I got. After opening the mp3 with audacity, right click on 
your mouse and select spectrogram option. You will get the password.
Now use that password to decrypt the rar file and then you will get a .txt file. 
View the text file, you'll get some base64 encoded text. Now combine the texts and decode that. You will get the flag

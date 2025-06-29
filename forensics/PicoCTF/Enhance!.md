# [Enhance!](https://play.picoctf.org/practice/challenge/265?category=4&page=3)

## Steps

1. **Download the File**  
   - Download the provided file: `drawing.flag.svg`.

2. **Inspect the File**  
   - Run `cat drawing.flag.svg` to view the contents of the SVG file.  
   - Look closely at the output, as it may contain the flag or a clue embedded in the SVG code (e.g., within text elements or comments).

3. **Identify and Clean the Flag**  
   - The challenge provides a flag with spaces: `picoCTF { 3 n h 4 n c 3 d _ d 0 a 7 5 7 b f }`.  
   - Use the command: `echo "picoCTF { 3 n h 4 n c 3 d _ d 0 a 7 5 7 b f }" | tr -d " "` to remove all spaces.  
   - **Output**: `picoCTF{3nh4nc3d_d0a757bf}`.

### Knight Switch Bank

1. **Download** the challenge file and make it executable:

   ```bash
   chmod +x filename
   ```

2. **Run** it once — you’ll see it just asks for a password.

3. **Open** the binary in Ghidra and look at the decompiled `main` function.

4. Inside `main`, you’ll spot a hardcoded string:

   ```c
   "ZRIU]HdANdJAGDIAxIAvDDsAyDDq_"
   ```

5. The program takes your input, applies **ROT13** (letters A–M / a–m get shifted forward by 13, N–Z / n–z go backward by 13), and then adds **+2** to every character.

6. To find the real password, just reverse that process. That means:

   * subtract 2, then undo ROT13, **or**
   * more simply, treat the stored string as a Caesar cipher and shift everything by `**+11**`.

7. Plug the string into any Caesar/ROT decoder with key 11, and you’ll get the correct flag.

## cbm-hackers's easy_reverse -> [Click](https://crackmes.one/crackme/5b8a37a433c5d45fc286ad83)


#### Steps to Solve:

1. Downloaded the challenge zip file.

2. Unzipped using:

   ```bash
   unzip file.zip
   ```

   (Password: `crackmes.one`)

3. Opened **Ghidra**:

   * New project → Named the project → Selected **non-shared** → Finished.
   * Dragged the binary into the project and **imported** it.

4. In the **Symbol Tree**, clicked on **Functions** → Opened `main`.

5. In the **Decompile** window:

   * Changed function signature to:

     ```c
     int main(int argc, int **argv)
     ```
   * Renamed `sVar1` to `length_check` (optional) since it holds the result of `strlen(argv[1])`.

6. Observed key logic:

   * Password must be **10 characters long**
   * **5th character must be '@'**
   * Otherwise, it prints usage

7. Tried:

   ```bash
   ./rev50_linux64-bit 1234@67890
   ```

---

#### Flag:

```
flag{1234@67890}
```

#  MacroHard WeakEdge - [Click](https://play.picoctf.org/practice/challenge/130?category=4&page=4&search=)


### 🧪 Steps to Solve:

1. **Download the file**:

   ```bash
   wget https://mercury.picoctf.net/static/2e739f9e0dc9f4c1556ea6b033c3ec8e/Forensics%20is%20fun.pptm
   ```

Then I opened the file but I couldn't found anything. So I searched online and found that `.pptm` files (macro-enabled PowerPoint files) are actually just **ZIP archives** under the hood — part of the [Open XML format](https://en.wikipedia.org/wiki/Office_Open_XML), used by Microsoft Office.
That means you can treat them like zip files and extract their internal structure using `unzip`. This lets you explore:

* **Macro code** (inside `vbaProject.bin`)
* **Slide data** and **hidden notes** (inside folders like `slides/`, `slideMasters/`)
* Other embedded or hidden content that may not appear in the normal PowerPoint UI
Since nothing was visible when the file was opened normally, it hinted that the flag might be hidden **in the structure**, not the visible content.*


2. **Unzip the `.pptm` file**:

   ```bash
   unzip Forensics\ is\ fun.pptm -d output_dir
   cd output_dir
   ```

3. Go into the `ppt` directory:

   ```bash
   cd ppt
   ```

4. Noticed a `vbaProject.bin` file (used for macros), but it didn’t have useful strings.

5. Checked `slideMasters/`:

   ```bash
   cd slideMasters
   ```

6. Found a suspicious file named `hidden`:

   ```bash
   cat hidden
   ```

7. Output looked like a space-separated **Base64** string:

   ```
   Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q
   ```

8. Cleaned it and decoded:

   ```bash
   echo "Z m x h Z z o g c G l j b 0 N U R n t E M W R f d V 9 r b j B 3 X 3 B w d H N f c l 9 6 M X A 1 f Q" | tr -d " " | base64 -d
   ```

---

### Flag:

```
picoCTF{D1d_u_kn0w_ppts_r_z1p5}
```



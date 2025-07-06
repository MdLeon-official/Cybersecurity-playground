# endianness-v2 - [Click](https://play.picoctf.org/practice/challenge/415?category=4&page=1&search=endianness)

### 🧪 Solution Steps

1. **Upload the File to CyberChef**:

   * Drag and drop the file into CyberChef’s input section.

2. **Convert to Hex**:

   * Use the "To Hex" operation so you can see and manipulate the raw hex values.

3. **Swap Endianness**:

   * Add the "Swap Endianness" operation.
   * Set **word length to 4 bytes (32 bits)**.
   * This reorganizes the bytes into the correct order.

4. **Inspect Magic Bytes**:

   * You should now see the JPEG header magic bytes:

     ```
     FF D8 FF E0 00 10 4A 46 49 46 00 01 (which is ÿØÿà␀␐JFIF␀␁)
     ```
   * This confirms it’s a **JPEG** file.

5. **Convert Back from Hex**:

   * Use the "From Hex" operation to return to binary form.

6. **Render the Image**:

   * The image should now display properly in CyberChef.
   * It shows a visual containing the **flag**.

---

### 🏁 Final Flag

```
picoCTF{cert!f1Ed_iNd!4n_*****_3nDian_f72c4bf7}
```

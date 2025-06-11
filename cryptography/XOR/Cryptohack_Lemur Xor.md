
# Lemur XOR

**🔗 Source:** [https://cryptohack.org/challenges/general/](https://cryptohack.org/challenges/general/)

---

## Challenge Description

I've hidden two cool images by XOR with the same secret key so you can't see them!
This challenge requires performing a **visual XOR between the RGB bytes** of two PNG images:

* `lemur.png`
* `flag.png`

---

## Approach

This is a classic image XOR problem. When two images are XORed with the **same key**, XORing them together removes the key:

```
(image1 ⊕ key) ⊕ (image2 ⊕ key)  
=> image1 ⊕ image2 ⊕ key ⊕ key  
=> image1 ⊕ image2  (since key ⊕ key = 0)
```

By XORing each RGB pixel of the two images, we cancel out the key and reveal the hidden image (usually the flag).

---

## Tools

* Python 🐍
* [Pillow (PIL)](https://pypi.org/project/Pillow/) for image handling
* XOR operation on RGB tuples pixel-by-pixel

---

## Code

```python
from PIL import Image

img1 = Image.open("lemur_ed66878c338e662d3473f0d98eedbd0d.png").convert("RGB")
img2 = Image.open("flag_7ae18c704272532658c10b5faad06d74.png").convert("RGB")
out = Image.new("RGB", img1.size)

for x in range(img1.width):
    for y in range(img1.height):
        p1 = img1.getpixel((x, y))
        p2 = img2.getpixel((x, y))
        out.putpixel((x, y), tuple(a ^ b for a, b in zip(p1, p2)))

out.show()
out.save("output.png")
```


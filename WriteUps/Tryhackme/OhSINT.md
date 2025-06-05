

# OhSINT

**Source:** [TryHackMe - OhSINT](https://tryhackme.com/room/ohsint)

---

## 📝 Challenge Description

> Are you able to use open source intelligence to solve this challenge?
> What information can you possible get with just one image file?

---

## 🔍 Initial Exploration

I began by analyzing the given image using `exiftool`:

```bash
exiftool image.jpg
```

This revealed the following key metadata:

* **Copyright:** `OWoodflint`

---

## 📱 Username Investigation

I searched `OWoodflint` on Google and found a profile on **X (Twitter)**.
The user's **avatar was a cat**.

✅ **Answer:** `cat`

---

## 🗺️ GPS Metadata

Exiftool also revealed GPS coordinates:

```
54 deg 17' 41.27" N, 2 deg 15' 1.33" W
```

When entered into Google Maps, this pinpoints to a location in the **UK**.

---

## 📡 BSSID Information

One post on @OWoodflint's X account included this Wi-Fi BSSID:

```
B4:5D:50:AA:86:41
```

I searched this on [Wigle.net](https://wigle.net/) and discovered:

* 📍 **City:** London
* 📶 **SSID:** UnileverWiFi

✅ **City Answer:** `London`
✅ **SSID Answer:** `UnileverWiFi`

---

## 📧 Email and Github

Google search for `OWoodflint` also led to a **GitHub profile**:

* GitHub page revealed **email address:** `owoodflint@gmail.com`

✅ **Answer:** `owoodflint@gmail.com`
✅ **Website where it was found:** `GitHub`

---

## 🌐 WordPress Blog

GitHub linked to a personal **WordPress blog**.

There, a post revealed vacation details:

✅ **Vacation location:** `New York`

---

## 🔐 Hidden Password

Inspecting the **source code** of the WordPress blog, I found the password:

✅ **Password:** `pennYDr0pper.!`


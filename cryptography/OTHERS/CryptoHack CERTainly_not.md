
# CERTainly not

*Source:* [https://cryptohack.org/challenges/general/](https://cryptohack.org/challenges/general/)

---

## Challenge Description

As mentioned in the previous challenge, PEM is just a nice wrapper above DER encoded ASN.1. In some cases you may come across DER files directly; for instance many Windows utilities prefer to work with DER files by default. However, other tools expect PEM format and have difficulty importing a DER file, so it's good to know how to convert one format to another.

An SSL certificate is a crucial part of the modern web, binding a cryptographic key to details about an organisation. We'll cover more about these and PKI in the TLS category. Presented here is a DER-encoded x509 RSA certificate. Find the modulus of the certificate, giving your answer as a decimal.

Challenge files:
  - 2048b-rsa-example-cert.der

---

## Approach

* Convert DER to PEM for easier parsing.
* Use `openssl` to extract the modulus (`n`) from the certificate.
* Convert the hex value of the modulus to decimal using Python.

---

## Tools

* `openssl` for format conversion and modulus extraction
* `Python` for hex to decimal conversion

---


### Convert DER to PEM:

```bash
openssl x509 -inform DER -in 2048b-rsa-example-cert.der -out der-to-pem.pem
```

### Extract modulus in HEX:

```bash
openssl x509 -in der-to-pem.pem -noout -modulus
```

### 🔢 Convert HEX to DEC in Python:

```python
modulus_hex = "Hex-Data"
modulus_dec = int(modulus_hex, 16)
print(modulus_dec)
```

---

**Flag / Answer:**
Submit the full decimal value printed by the Python script.

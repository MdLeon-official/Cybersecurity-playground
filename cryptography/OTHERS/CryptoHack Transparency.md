
# Transparency

### Challenge:

Attached is an RSA public key in PEM format. Find the subdomain of cryptohack.org which uses these parameters in its TLS certificate, and visit that subdomain to obtain the flag.

Challenge files:
  - transparency.pem


---

### Steps Taken:

1. **Understanding the Task:**

   * The challenge provides a public RSA key.
   * The goal is to identify which subdomain of `cryptohack.org` uses a TLS certificate containing this exact key.
   * Once the matching subdomain is found, visiting it will reveal the flag.

2. **Enumerating Subdomains:**

   * Used an online subdomain enumeration tool:
     [https://subdomains.whoisxmlapi.com](https://subdomains.whoisxmlapi.com)
     to list all subdomains under `cryptohack.org`.
   * Among many results, one subdomain stood out:
     `thetransparencyflagishere.cryptohack.org`

3. **Verifying the Subdomain:**

   * Visited `https://thetransparencyflagishere.cryptohack.org`
   * The page contained the flag:
     `crypto{thx_redpwn_for_inspiration}`


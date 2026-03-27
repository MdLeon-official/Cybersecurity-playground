# What Is JSON

**JavaScript Object Notation(JSON)** , text based format for transmitting data across the web application. It stores information in a easy to access manner for both the developer and the computer. Can work with many programming language and preferred syntax for API.

# What is JWT

**JSON Web Token** is a compact, URL-safe means of representing claims to be transferred between two parties

# JWT Formats

A JWT consists of 3 parts separated by dots:
```
Header.Payload.Signature
```

**Header:** Base64URL-encoded JSON, Contains metadata: alg → signing algorithm (e.g., RS256, HS256), kid → key ID (optional)

**Payload:** Base64URL-encoded JSON, Contains user data, Readable and modifiable by anyone, NOT encrypted

**Signature:** Generated using: `Header + Payload + Secret/Private Key`, Ensures integrity (no tampering) &
authenticity (issued by trusted server)


# JWT vs JWS vs JWE

| Feature                               | JWT                               | JWS                                   | JWE                                       |
| ------------------------------------- | --------------------------------- | ------------------------------------- | ----------------------------------------- |
| **What it is**                        | A **format/structure** for tokens | A **signed token** (JWT + signature)  | An **encrypted token** (JWT + encryption) |
| **Think of it as**                    | A **box**                       | A box with a **tamper-proof seal**  | A box that is **locked**                |
| **Main purpose**                      | Carry data (claims)               | Make sure data is **not changed**     | Make sure data is **hidden**              |
| **Security by itself**                |  None                            |  Signature protection                |  Encryption protection                   |
| **Can you read data?**                | Depends                           |  Yes (anyone can decode)             |  No (encrypted)                          |
| **Can data be modified?**             | Yes (no protection)               | Yes, but signature will break        | No (cannot read/modify easily)            |
| **Integrity (tamper check)**          |  No                              |  Yes                                 |  Yes                                     |
| **Confidentiality (privacy)**         |  No                              |  No                                  |  Yes                                     |
| **Used in real apps**                 | As a concept                      |  Very common (login tokens)          |  Rare                                   |
| **What people usually mean by “JWT”** | General term                      |  Actually JWS                       | Rarely JWE                                |


JWTs are self-contained tokens, meaning the server does not store their original data and fully relies on the signature to check if they are valid. If the server does not properly verify the signature, it has no way to detect changes in the token. This allows an attacker to modify the payload, such as changing the username to impersonate another user or setting isAdmin to true to gain higher privileges. Since the server trusts the token, it may accept these changes as legitimate.

## Accepting arbitrary signatures

JWT libraries usually provide two functions: one to verify a token and one to just decode it. The verify() function checks the signature and makes sure the token is valid and not tampered with. The decode() function only reads the data inside the token without checking if it is real. If a developer mistakenly uses decode() instead of verify(), the application does not validate the signature at all. This means an attacker can create or modify a token however they want, and the server will still accept it as valid.

<br>

- **Lab: JWT authentication bypass via unverified signature** - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/JWT%20attacks/JWT_Labs.md#lab-jwt-authentication-bypass-via-unverified-signature)

<br>

## Accepting tokens with no signature

JWT has a field called `alg` that tells the server how the token is signed. The problem is this value comes from the user, so it can be changed. An attacker can set `alg` to `none`, which means no signature is used. If the server accepts this, it stops checking the signature completely. This allows the attacker to change the token however they want, like becoming an admin, and the server will still trust it. In simple terms, the server is trusting what the attacker says about security, which leads to a full authentication bypass.

<br>

- **Lab: JWT authentication bypass via flawed signature verification** - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/JWT%20attacks/JWT_Labs.md#lab-jwt-authentication-bypass-via-flawed-signature-verification)

<br>

## Brute-forcing secret keys
In algorithms like HS256, the server uses a secret key to sign the JWT. This key works like a password. If the secret is weak, common, or not changed from a default value, an attacker can guess it using brute force. Once the attacker finds the correct secret, they can create their own JWT with any data they want, such as making themselves an admin, and sign it with a valid signature.

### Brute-forcing secret keys using hashcat
```
hashcat -a 0 -m 16500 <jwt> <wordlist>
```

- **Lab: JWT authentication bypass via weak signing key** - [SOLUTION](https://github.com/OxL3on/Cybersecurity-playground/blob/main/PORTSWIGGER%20labs/JWT%20attacks/JWT_Labs.md#lab-jwt-authentication-bypass-via-weak-signing-key)


# JWT header parameter injections

The JWT header (JOSE header) can contain parameters that specify how the token’s signature should be verified. The three most relevant for attacks are:

- **jwk (JSON Web Key)** - embeds the public key directly inside the header.  
- **jku (JSON Web Key Set URL)** - points to a URL where the server retrieves the key set.  
- **kid (Key ID)** - references a specific key by an identifier.

An attacker can modify these parameters to substitute their own key. By signing the token with a key they control and instructing the server to use that same key (via jwk, jku, or kid), they can make the server accept a forged token. Successful exploitation relies on the server trusting these user‑supplied header fields without validation.


### Injecting self-signed JWTs via the jwk parameter
The `jwk` header parameter allows a public key to be embedded directly inside the JWT. If a server is misconfigured to accept any key presented in `jwk`, an attacker can:
Generate their own RSA key pair. Modify the JWT payload. Sign the token with their private key. Insert the matching public key (as a JWK) into the header.

The server will use the attacker‑supplied public key to verify the signature, accepting the forged token as valid. Tools like the JWT Editor extension automate embedding the key and adjusting the `kid` parameter.

- **Lab: JWT authentication bypass via jwk header injection** - [SOLUTION]()

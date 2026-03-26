## What Is JSON

**JavaScript Object Notation(JSON)** , text based format for transmitting data across the web application. It stores information in a easy to access manner for both the developer and the computer. Can work with many programming language and preferred syntax for API.

## What is JWT

**JSON Web Token** is a compact, URL-safe means of representing claims to be transferred between two parties

## JWT Formats

A JWT consists of 3 parts separated by dots:
```
Header.Payload.Signature
```

**Header:** Base64URL-encoded JSON, Contains metadata: alg → signing algorithm (e.g., RS256, HS256), kid → key ID (optional)

**Payload:** Base64URL-encoded JSON, Contains user data, Readable and modifiable by anyone, NOT encrypted

**Signature:** Generated using: `Header + Payload + Secret/Private Key`, Ensures integrity (no tampering) &
authenticity (issued by trusted server)


## JWT vs JWS vs JWE

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

### Accepting arbitrary signatures

JWT libraries usually provide two functions: one to verify a token and one to just decode it. The verify() function checks the signature and makes sure the token is valid and not tampered with. The decode() function only reads the data inside the token without checking if it is real. If a developer mistakenly uses decode() instead of verify(), the application does not validate the signature at all. This means an attacker can create or modify a token however they want, and the server will still accept it as valid.

<br>

- **Lab: JWT authentication bypass via unverified signature**

<br>

# Excessive Data Exposure

`{{baseUrl}}/community/api/v2/community/posts/recent` -> this location gives more data that it was asked for (name, email ... etc)

# JWT

Get JWT after login  ->  find public RSA key in `/.well-known/jwks.json`  ->  convert JWK to PEM → Base64‑encode PEM (watch whitespace & padding)  ->  create symmetric key with that Base64 as HMAC secret  ->  forge JWT: change `alg` to `HS256`, set `sub` to `email found in Excessive data exposer`, sign with the symmetric key  ->  Get access to that account



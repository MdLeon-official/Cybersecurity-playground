# OAuth
OAuth is a way for apps to get limited access to our account on another service without seeing our password. Instead of giving your login details, you simply approve what the app can access, like your email or profile. This keeps your credentials safe and gives you control over what data is shared. It’s commonly used when you click things like “Login with Google” or “Login with Facebook,” where one service verifies you for another without exposing your password.

# How does OAuth 2.0 work?
There are three main roles involved. **The client** is the app that wants your data, **the resource owner** is you, and **the OAuth provider** is the service that actually holds your data, like Google or Facebook. 
Here’s how it works: First, the app asks for access to certain data, like your profile or contacts. Then you’re redirected to the provider’s login page, where you sign in and approve what the app is asking for. After that, the provider gives the app a special token instead of your password. This token acts like a temporary key. Finally, the app uses that token to request your data from the provider.

# OAuth grant types
An OAuth grant type is just the way an app gets permission and receives an access token. It defines how the process works between the app, the user, and the OAuth service.

## OAuth scopes
OAuth scopes are what an app asks permission for. They define what data the app can access and what it can do with it, like reading your contacts or accessing your profile. The app includes these scopes when requesting access, and you approve them.
Different services use different names for scopes, but the idea is always the same: scopes limit what the app is allowed to do.

## Authorization code grant type
Authorization code grant type is a secure way for an app to access your data.
To initiate the flow first the client applicatio and OAuth service exchange some http requests. 
Then you log in and approve access. The app gets an authorization code, then sends it to the OAuth server. Along with this, it also sends a **client_secret** to prove its identity.
The server verifies this and returns an access token. Since this exchange happens server-to-server and includes the client_secret, it’s considered very secure.
Here are clean, exam-friendly notes for each OAuth step 👇

**Step 1: Authorization Request**

Client app sends request to OAuth server (`/authorization` or `/auth`), Goal: Ask permission to access user data, Uses browser (front-channel)
```
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```
`client_id` → Unique ID of client app. `redirect_uri` → Where user is sent after auth (callback URI), `response_type=code` → Indicates Authorization Code flow, `scope` → What data is requested (e.g., profile, email), `state` → Random value to prevent CSRF attacks

**Step 2: User Login & Consent**

User is redirected to OAuth provider login page, User logs in and approves requested permissions.
Based on `scope`, user sees what data is requested, Consent may be skipped if already approved before, Uses user session (cookies)

**Step 3: Authorization Code Grant**

After approval, user is redirected back to client (`redirect_uri`)
```
GET /callback?code=a1b2c3d4e5f6g7h8&state=ae13d489bd00e3c24 HTTP/1.1
Host: client-app.com
```
`code` → Temporary authorization code, `state` → Must match original (CSRF protection)

**Step 4: Access Token Request**

Client server sends POST request to `/token` endpoint, This is server-to-server (back-channel) → more secure
```
POST /token HTTP/1.1
Host: oauth-authorization-server.com
…
client_id=12345&client_secret=SECRET&redirect_uri=https://client-app.com/callback&grant_type=authorization_code&code=a1b2c3d4e5f6g7h8
```
`client_secret` → Proves client identity, `code` → Received from previous step, 

**Step 5: Access Token Grant**

OAuth server validates request, Sends back an **access token**
```
{
    "access_token": "z0y9x8w7v6u5",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid profile",
    …
}
```
`access_token` → Used to access user data, `token_type` → Usually Bearer, `expires_in` → Token lifetime, `scope` → Approved permissions

**Step 6: API Call**

Client uses access token to request user data.
First, Sends request to `/userinfo` or API endpoint. Includes token in header:

```
Authorization: Bearer <access_token>
```

**Step 7: Resource Grant**

Resource server verifies token, If valid → returns user data
```
{
    "username":"carlos",
    "email":"carlos@carlos-montoya.net",
    …
}
```


> Authorization → Login → Code → Token → API → Data → Login



## Implicit grant type
After user login & consent, the client immediately receives the access token (no authorization code step) via browser redirect. Since no back-channel & no client_secret → all happens in front-channel so it is less secure (token exposed in browser)
Used in SPA / mobile apps where secret storage isn’t possible


**Step 1: Authorization Request**

Client sends request with `response_type=token`, Same as auth code flow but asks for **token directly**


**Step 2: User Login & Consent**

User logs in and approves permissions, Same process as authorization code flow


**Step 3: Access Token Grant**

OAuth server redirects to `redirect_uri`, Sends **access token in URL fragment (`#`)**, not query

```
GET /callback#access_token=z0y9x8w7v6u5&token_type=Bearer&expires_in=5000&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
```
Token is handled by browser (JS extracts it)


**Step 4: API Call**

Client uses extracted token, Sends request with:

```
Authorization: Bearer <access_token>
```


**Step 5: Resource Grant**

Server verifies token, Returns user data (email, username, etc.)



> Login → Token (direct) → API → Data → Login session





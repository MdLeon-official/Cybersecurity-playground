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

https://portswigger.net/web-security/images/oauth-authorization-code-flow.jpg

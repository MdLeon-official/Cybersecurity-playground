## [Lab: SQL injection vulnerability allowing login bypass](https://portswigger.net/web-security/sql-injection/lab-login-bypass)

#### **Steps to Solve:**

1. Click **"ACCESS THE LAB"** to launch the challenge.
2. Navigate to the **"My Account"** login page.
3. For the username, enter:

   ```
   administrator'--
   ```
4. Leave the password field blank (or enter anything).
5. Submit the form – you're now logged in as administrator, and the lab is marked as solved!

#### Key Notes:

* `'--` is a classic **SQL injection** payload to comment out the rest of the SQL query.
* This bypass works because the SQL statement becomes something like:

  ```sql
  SELECT * FROM users WHERE username = 'administrator'--' AND password = '...';
  ```
* This attack works when input is **not sanitized** and is **directly injected into SQL queries**.

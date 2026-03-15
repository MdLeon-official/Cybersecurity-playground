### [Lab: SQL injection attack, querying the database type and version on Oracle](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle)

---

#### 🧪 Steps to Solve:

1. Clicked on **Gifts** to trigger a request with category filter.
2. Intercepted the request with **Burp Suite**.
3. Tested the number of columns using `ORDER BY`:

   * `' ORDER BY 1--` ✅
   * `' ORDER BY 2--` ✅
   * `' ORDER BY 3--` ❌ → means **2 columns**
4. Tested data types with:

   ```
   ' UNION SELECT NULL, 'a' FROM DUAL--
   ```

   ✅ Page loaded successfully, means 2nd column accepts string.
5. Fetched database version:

   ```
   ' UNION SELECT banner, NULL FROM v$version--
   ```

   ✅ Output showed Oracle version → Lab Solved.

---

#### Key Notes:

* `DUAL` is a special table in Oracle used when no real table is needed.
* `v$version` is an Oracle system view showing DB version info.
* `ORDER BY N--` helps find number of columns.
* Use `NULL` for unknown data types during testing.

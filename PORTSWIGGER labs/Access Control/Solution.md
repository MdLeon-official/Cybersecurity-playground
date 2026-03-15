# Access Control Labs

### 1. Lab: Unprotected admin functionality

Checked `robots.txt` and found `/administrator-panel`.
Opened it directly and deleted user `carlos`.

---

### 2. Lab: Unprotected admin functionality with unpredictable URL

Checked `robots.txt` but found nothing.
Viewed the page source and found the admin URL in a JavaScript file: `/admin-imd2oc`.

---

### 3. Lab: User role controlled by request parameter

Logged in with the provided normal user credentials.
In the cookies I saw `Admin=false`.
Changed it to `Admin=true` and refreshed the page to access admin functionality.

---

### 4. Lab: User role can be modified in user profile

Changed the email field and captured the request in Burp.
The response showed `roleid=1`.
Added `roleid=2` in the request along with the email and sent it again to become admin.

---

### 5. Lab: User ID controlled by request parameter

Logged in as `wiener`.
In the URL, changed `id=wiener` to `id=carlos` to access Carlos's account.

---

### 6. Lab: User ID controlled by request parameter, with unpredictable user IDs

The URL contained a GUID like:

```
id=48025664-801e-4f32-a7b3-35417e3b6c7f
```

which belonged to `wiener`.

Found Carlos's GUID in one of the blog posts and replaced the ID with that value.

---

### 7. Lab: User ID controlled by request parameter with data leakage in redirect

Changing `id=wiener` to `id=carlos` redirected to the login page.

Captured the request in Burp and followed the redirect manually to see Carlos's data.

---

### 8. Lab: User ID controlled by request parameter with password disclosure

Changed `id` to `administrator`.

The password was hidden in the browser, so I captured the request in Burp and checked the response, which revealed the password.
Used it to log in as `administrator`.

---

### 9. Lab: Insecure direct object references

The application had a live chat feature where transcripts could be downloaded.

Download links started from `2.txt`.
Captured the request and changed the file name to `1.txt` to access another user's transcript.

---

### 10. Lab: URL-based access control can be circumvented

The application used the `X-Original-URL` header.

Captured the request for the admin panel and modified it:

```
X-Original-URL: /admin
```

Removed `/admin` from the main URL.

To delete Carlos:

```
X-Original-URL: /admin/deleteUser
/?username=carlos
```

---

### 11. Lab: Method-based access control can be circumvented

The goal was to promote my user (`wiener`) to admin.

Captured the request used to promote `carlos`.
Changed the request method from `POST` to `GET` and used `wiener`'s session cookie with `username=wiener`.

---

### 12. Lab: Multi-step process with no access control on one step

Similar to the previous lab.
The application used multiple steps for the action, but one step lacked proper access control.
By sending the request directly for that step, the action could be completed.

---

### 13. Lab: Referer-based access control

The application relied on the `Referer` header for access control.

Captured the request in Burp and added the required `Referer` header manually to bypass the restriction.

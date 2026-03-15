# Lab: Stored XSS into HTML context with nothing encoded - [Click](https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded)

### Vulnerability:
This lab contains a stored cross-site scripting vulnerability in the comment functionality.
To solve this lab, submit a comment that calls the alert function when the blog post is viewed.


### Step-by-step:

1. **Access the lab**

2. Click any **"View post"**

3. Scroll down to the **comment section**

4. Submit the following payload in the comment form:

   ```html
   <script>alert(1)</script>
   ```

5. Fill in the **Name**, **Email**, and **Website** fields with any value

6. Click **"Post comment"**

7. Return to the blog or refresh — your payload is executed!


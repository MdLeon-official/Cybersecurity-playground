# What is SSRF

SSRF is a vulnerability class that occurs when an application is fetching a remote resource without first validating the user-spplied URL.
There are 2 types:
1. Regular/In Band
2. Blind/Out-of-Band

# How to Find SSRF:
 - Map The Application
     - Identify any request parameters that contains hostnames, IP addresses or full URLs
       
 - For each request parameter, modify its value to specify an alternative resource and observe how the application responds

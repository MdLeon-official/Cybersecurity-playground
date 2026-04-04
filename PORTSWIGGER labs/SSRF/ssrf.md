## What is SSRF

SSRF is a vulnerability class that occurs when an application is fetching a remote resource without first validating the user-spplied URL.
There are 2 types:
1. Regular/In Band
2. Blind/Out-of-Band

##
How to Find SSRF:
 - Map The Application
     - Identify any request parameters that contains hostnames, IP addresses or full URLs
       
 - For each request parameter, modify its value to specify an alternative resource and observe how the application responds
     - If a defense is in place, attempt to circumvent it using know techniques

 - For each request parameter, modify its value to a server on the internet that you control and monitor the server for incoming requests
     - If no incoming connections are received, monitor the time taken for the application to        respond

## How to exploit SSRF

1. **Regular/In-Band SSRF:**
   - If the application allows for user-supplied arbitary URLs, try:
     - Determine if a port number can be specified
     - If successful, attempt to port-scan the internal network using Burp Intruder
     - Attempt to connect to other services on the loopback address

   - If the application doesn't allow for arbitary user-supplied URLs, try to bypass defenses using:
      - Use different encoding schemes
      - Register a domain name that resolves to internal IP address (DNS Rebinding)
      - Use your own server that redirects to an internal IP address (HTTP Redirection)
      - Exploit inconsistencies in URL parsing
    
2. **Blind/Out-of-Band SSRF:**
   - If the application is vulnerable to blind SSRF, try to exploit using:
     - Attempt to trigger an HTTP request to an external system you control and monitor the system for network interactions from the vulnerable server.
         - If defenses are put in place, follow previous techniques.
         - Exploit inconsistencies in URL parsing
      


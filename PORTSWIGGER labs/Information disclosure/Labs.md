 # Files for web crawlers

 # Directory listings

 # Developer comments


# Error messages

Verbose errors reveal expected input types, data formats, and exploitable parameters. They expose technology stacks (template engines, databases, servers, versions) - helps find known exploits or misconfigurations. Open‑source frameworks - study public source code for custom exploits. Differences in error messages indicate backend behavior (e.g., SQL injection, username enumeration).

- Lab: Information disclosure in error messages

The /product endpoint expects an integer value for the productId parameter. When I supplied a non‑integer value (e.g., a string), the application returned a verbose error message that inadvertently disclosed the version number of a third‑party framework. This revealed the technology stack, completing the lab.

# Debugging data

Debugging data is a rich source of information disclosure when left in production. Custom error messages and debug logs can leak session variables, backend hostnames and credentials, server file paths, encryption keys, or access to separate debug files. Attackers use this data to understand application state and craft inputs that manipulate behavior.

# What are business logic vulnerabilities?

Business logic vulnerabilities are flaws in an application's rules that allow users to perform unintended actions. These issues do not come from technical errors like SQL injection but from incorrect or incomplete design of how the system should behave. Attackers exploit these flaws by interacting with the application in ways developers did not expect.

Business logic defines how an application works, such as enforcing payment before access, limiting coupon usage, or maintaining a proper workflow. When these rules are not properly enforced, users may bypass restrictions, skip steps, or manipulate important values like price or quantity.

These vulnerabilities are difficult to detect with automated tools because they require understanding the application's intended behavior and thinking creatively about how it can be misused. As a result, they are commonly found through manual testing and are a major focus in bug bounty programs.

In simple terms, business logic vulnerabilities occur when an application follows flawed rules, allowing attackers to abuse normal functionality for malicious purposes.


# Examples of business logic vulnerabilities

## Excessive trust in client-side controls

Excessive trust in client-side controls happens when an application relies on browser-side validation to secure user input. Developers assume users will only interact through the web interface, but attackers can intercept and modify requests using tools like Burp Suite, bypassing these controls. Since client-side validation can be easily ignored, accepting data without proper server-side checks allows attackers to manipulate inputs such as price, quantity, or permissions. This can lead to serious security and business impact. In short, client-side controls are not trustworthy, and all critical validation must be enforced on the server side.

- Lab: Excessive trust in client-side controls - [SOLUTION]()
- Lab: 2FA broken logic - [SOLUTION]()

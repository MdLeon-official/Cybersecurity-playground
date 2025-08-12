# **Challenge Name: Getting Started**

1. Download the challenge file (`getting-started`).
2. Run the `strings` command to extract readable text:

   ```bash
   strings getting-started
   ```
3. One suspicious string appears:

   ```
   j}j1j_jljejvjejlj_jojtj_jejmjojcjljejwj{jgjajljf
   ```
4. Open a code editor and create a Python script:

   ```python
   gs_str = "j}j1j_jljejvjejlj_jojtj_jejmjojcjljejwj{jgjajljf"
   replace_str = gs_str.replace("j", "")
   print(replace_str[::-1])
   ```
5. Run the script to get the flag.

**Flag:** `flag{welcome_to_level_1}`

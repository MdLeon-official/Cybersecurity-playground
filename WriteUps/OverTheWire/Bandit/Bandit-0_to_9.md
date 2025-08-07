## **Bandit Level 0 → Level 1**

**Connect using SSH:**

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
ls
cat readme
```

**Password for Level 1:**

```
ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If
```

---

## **Bandit Level 1 → Level 2**

**Connect:**

```bash
ssh bandit1@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
ls
cat ./-
```

**Password for Level 2:**

```
263JGJPfgU6LtdEvgfWU1XP5yac29mFx
```

---

## **Bandit Level 2 → Level 3**

**Connect:**

```bash
ssh bandit2@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
ls
cat ./--spaces\ in\ this\ filename--
```

**Password for Level 3:**

```
MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx
```

---

## **Bandit Level 3 → Level 4**

**Connect:**

```bash
ssh bandit3@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
ls
cd inhere
cat ...Hiding-From-You
```

**Password for Level 4:**

```
2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ
```

---

## **Bandit Level 4 → Level 5**

**Connect:**

```bash
ssh bandit4@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
cd inhere
file ./*
cat ./-file07
```

**Password for Level 5:**

```
4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw
```

---

## **Bandit Level 5 → Level 6**

**Connect:**

```bash
ssh bandit5@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
cd inhere
find . -type f -size 1033c -not -executable -exec file {} + | grep ASCII
cat ./maybehere07/.file2
```

**Password for Level 6:**

```
HWasnPhtq9AVKe0dmk45nxy20cvUa6EG
```

---

## **Bandit Level 6 → Level 7**

**Connect:**

```bash
ssh bandit6@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
find / -type f -size 33c -user bandit7 -group bandit6 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

- *2>/dev/null → hide permission denied errors*

**Password for Level 7:**

```
morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj
```

---

## **Bandit Level 7 → Level 8**

**Connect:**

```bash
ssh bandit7@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
cat data.txt | grep millionth
```

**Password for Level 8:**

```
dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc
```

---

## **Bandit Level 8 → Level 9**

**Connect:**

```bash
ssh bandit8@bandit.labs.overthewire.org -p 2220
```

**Command:**

```bash
sort data.txt | uniq -u
```

**Password for Level 9:**

```
4CKMh1JI91bUIZZPXDqGanal4xvAg0JM
```

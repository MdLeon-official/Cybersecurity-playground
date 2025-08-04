## Reverse Engineering Challenge #1 - [Click](https://challenges.re/1/)

### What the function does:

```asm
<f>:
  0:  mov    r8, rdi       ; Save source pointer (arg1)
  3:  push   rbx           ; Save rbx (callee-saved)
  4:  mov    rdi, rsi      ; rdi = destination pointer (arg2)
  7:  mov    rbx, rdx      ; rbx = divisor (arg3)
  a:  mov    rsi, r8       ; rsi = source pointer
  d:  xor    rdx, rdx      ; Clear rdx before division (needed for div)

begin:
 10:  lods   rax, [rsi]    ; Load 8 bytes from [rsi] into rax, rsi += 8
 12:  div    rbx           ; Unsigned divide rdx:rax by rbx → quotient in rax, remainder in rdx
 15:  stos   [rdi], rax    ; Store quotient in [rdi], rdi += 8
 17:  loop   begin         ; Decrement rcx, jump to 'begin' if rcx ≠ 0
 19:  pop    rbx           ; Restore original value of rbx
 1a:  mov    rax, rdx      ; Move last remainder into rax
 1d:  ret
```


### Function Arguments

| Register | Meaning             |
| -------- | ------------------- |
| rdi      | Source pointer      |
| rsi      | Destination pointer |
| rdx      | Divisor             |
| rcx      | Number of elements  |


### What this function does overall:

1. It divides each 64-bit integer from the source array by the divisor.
2. Stores each quotient into the destination array.
3. After processing all elements, it returns the last remainder in `rax`.

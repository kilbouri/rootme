## Important Storage Locations

### `user_input`: `fp@main + 0x1c`

The following assembly allows us to determine the location of `user_input` (which is `char[]`):

```x86asm
;-- load_user_input_ptr_into_v0:
0x004008cc      addiu   v0, fp, 0x1c
0x004008d0      move    a0, v0
;-- load_buffer_size_into_a1:
0x004008d4      addiu   a1, zero, 0x40
0x004008d8      move    a2, v1
;-- load_fgets_ptr_into_t9:
0x004008dc      lw      t9, -fgets(gp)
0x004008e0      nop
;-- invoke_fgets:
0x004008e4      jalr    t9         ; fgets(0x40, &user_input) / fgets(0x40, fp + 0x1c)
```

## Correct Password is 19 Characters

Once [`user_input`](#user_input-fpmain--0x1c) has been read via `fgets`, the following assembly is run to check its length:

```x86asm
;-- load_user_input_ptr_into_a0:
0x0040091c      addiu   v0, fp, 0x1c
0x00400920      move    a0, v0
;-- load_strlen_ptr_into_t9:
0x00400924      lw      t9, -strlen(gp) ; 0x410d6c
0x00400928      nop
;-- invoke_strlen:
0x0040092c      jalr    t9         ; v0 = strlen(user_input)
0x00400930      nop
0x00400934      lw      gp, (var_60h)
;-- save_strlen_result_in_v1:
0x00400938      move    v1, v0
;-- set_v0_eq_19:
0x0040093c      addiu   v0, zero, 0x13
;-- is_string_19_chars:
0x00400940      beq     v1, v0, length_check_passed
0x00400944      nop
0x00400948      jal     invalid_pass ; invalid_pass ; void invalid_pass(int32_t arg1)
0x0040094c      nop
0x00400950      lw      gp, (var_60h)
0x00400954      sw      zero, (var_10h)
0x00400958      b       0x400b64
0x0040095c      nop
;-- length_check_passed:
```

## Correct Password has `8..=17 == 'i'`

```x86asm
;-- length_check_passed:
0x00400960      addiu   v0, zero, 8
0x00400964      sw      v0, (i)    ; init loop counter i = 8
0x00400968      b       check_loop_condition
0x0040096c      nop
;-- loop_body:
0x00400970      lw      v1, (i)    ; v1 = i
0x00400974      addiu   v0, fp, 0x18 ; v0 = &user_input - 4
0x00400978      addu    v0, v0, v1 ; v0 = &user_input + i - 4
0x0040097c      lb      v1, 4(v0)  ; v1 = *(&user_input + i - 4 + 4)
0x00400980      addiu   v0, zero, 0x69 ;  'i'
0x00400984      beq     v1, v0, loop_increment ; user_input[i] == 'i'
0x00400988      nop
0x0040098c      jal     invalid_pass ; invalid_pass ; void invalid_pass(int32_t arg1)
0x00400990      nop
0x00400994      lw      gp, (var_60h)
0x00400998      sw      zero, (var_10h)
0x0040099c      b       0x400b64
0x004009a0      nop
;-- loop_increment:
0x004009a4      lw      v0, (i)
0x004009a8      nop
0x004009ac      addiu   v0, v0, 1
0x004009b0      sw      v0, (i)
;-- check_loop_condition:
0x004009b4      lw      v0, (i)
0x004009b8      nop
0x004009bc      slti    v0, v0, 0x11 ; v0 = i < 0x11
0x004009c0      bnez    v0, loop_body ; b if v0 != 0 (i < 0x11)
;-- end_of_loop:
```

## Correct Password has Specific Values at Specific Indices

Having spent some time working out what was where on the stack, we have the following stack layout:
```x86asm
; arg int argc @ a0
; arg char **argv @ a1
; var int32_t old_global_pointer @ stack - 0x60
; var int32_t i @ stack - 0x58
; var int32_t user_input @ stack - 0x54
; var int32_t user_input_at_4 @ stack - 0x50
; var int32_t user_input_at_5 @ stack - 0x4f
; var int32_t user_input_at_7 @ stack - 0x4d
; var int32_t user_input_at_17 @ stack - 0x43
; var int32_t stack_0x10 @ stack - 0x10
; var int32_t stack_0x0c @ stack - 0xc
; var int32_t old_frame_pointer @ stack - 0x8
; var int32_t old_return_address @ stack - 0x4
```

Note that we have multiple references into `user_input`. The index they correspond to is trivially calculated by comparing the
reference's location (e.g. `stack - 0x50`) to `user_input`'s location, `stack - 0x54`. `0x54 - 0x50 = 0x4` so the index is `4`.

We can now turn our attention back to the decompiled output, and take advantage of the newly named locations to interpret the
remaining comparisons:
```c
if (user_input_at_17._1_1_ == 's') {
    if ((char)user_input_at_17 == 'p') {
        if ((char)user_input_at_7 == 'm') {
            if ((user_input._2_1_ == 'n') && (cStack_4e == 'n')) {
                if ((char)user_input == 'c') {
                    if (user_input._1_1_ == 'a') {
                        if (user_input._3_1_ == 't') {
                            if (user_input_at_4 == 'r') {
                                if (user_input_at_5 == 'u') {
                                    valid_pass((int32_t)arg1);
```

The funky `x._2_1_` syntax is indicating an array access. Specifically, in the case of `x._2_1_`, it is saying the equivalent to
`*((char*)&x + 2)`. That is, offset `2` bytes from `x` and read `1` byte. So whenever we see `user_input._Y_1_`, we can read it as
`user_input[Y]` (likewise, `user_input_at_X._Y_1_` is `user_input_at_X[Y]`).

Also, in the decompiled output, we see that Rizin has decided to pull out an additional local, `cStack_4e`, which is stored at `stack - 0x4e`.
That makes it `user_input_at_6`.

Therefore, we have the following additional information about the password:

```c
password[17 + 1] = 's'
password[17] = 'p'
password[7] = 'm'
password[2] = 'n'
password[6] = 'n' // recall: `cStack_4e = stack - 0x4e = user_input[6]` because `user_input[7]` is `stack - 0x4f`
password[0] = 'c'
password[1] = 'a'
password[3] = 't'
password[4] = 'r'
password[5] = 'u'

// in array order:

password[0] = 'c'
password[1] = 'a'
password[2] = 'n'
password[3] = 't'
password[4] = 'r'
password[5] = 'u'
password[6] = 'n'
password[7] = 'm'
password[17] = 'p'
password[17 + 1] = 's'
```

## Conclusion

We have two partial views of the correct password: [`????????iiiiiiiii??`](#correct-password-has-817--i) and [`cantrunm?????????ps`](#correct-password-has-specific-values-at-specific-indices).

Overlaying them gives the password in cleartext:

```
????????iiiiiiiii??
cantrunm?????????ps
-------------------
cantrunmiiiiiiiiips
```

The password is `cantrunmiiiiiiiiips`!

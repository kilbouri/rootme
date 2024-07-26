Using Cutter's Ghidra decompiler we can find the following code to check the password:

```c
counter = -input_len + 6;

if (input[0] != input[5]) {
    counter = -input_len + 7;
}

if (input[0] + 1 != (uint32_t)input[1]) {
    counter += 1;
}

if (input[3] + 1 != (uint32_t)input[0]) {
    counter += 1;
}

if (input[2] + 4 != (uint32_t)input[5]) {
    counter += 1;
}

if (input[4] + 2 != (uint32_t)input[2]) {
    counter += 1;
}

int checksum = counter + (input[3] ^ 0x72) + (uint32_t)input[6];
if (checksum == 0) {
    puts("Success, you rocks!");
    exit(0);
}
```

An earlier check ensures the input length is exactly `6`. Thus we can simplify a few parts of the code:

```c
counter = 0

if (input[0] != input[5]) {
    counter = 1
    // must be skipped to ensure counter = 0
}

if (input[0] + 1 != (uint32_t)input[1]) {
    counter += 1;
    // must be skipped to ensure counter = 0
}

if (input[3] + 1 != (uint32_t)input[0]) {
    counter += 1;
    // must be skipped to ensure counter = 0
}

if (input[2] + 4 != (uint32_t)input[5]) {
    counter += 1;
    // must be skipped to ensure counter = 0
}

if (input[4] + 2 != (uint32_t)input[2]) {
    counter += 1;
    // must be skipped to ensure counter = 0
}

int checksum = counter + (input[3] ^ 0x72) + (uint32_t)0; // since len(input) == 6,
                                                          // input[6] is '\0
if (checksum == 0) {
    puts("Success, you rocks!");
    exit(0);
}
```

This gives the following constraints:
- `input[0] + 0 == input[5]`
- `input[0] + 1 == input[1]`
- `input[3] + 1 == input[0]`
- `input[2] + 4 == input[5]`
- `input[4] + 2 == input[2]`
- `input[3] ^ 0x72 == 0` thus `input[3] = 0x72`

What a nice recipe! Simple arithmetic gives us the following input bytes: `[0x73, 0x74, 0x6F, 0x72, 0x6D, 0x73]`. Therefore the password is `storms`!

"""
Python translation of the following GDScript extracted from
the binary using `strings 0_protection.exe | grep -A 10 -B 10 _ready`

```
var key = [119, 104, 52, 116, 52, 114, 51, 121, 48, 117, 100, 48, 49, 110, 103, 63]
var enc = [32, 13, 88, 24, 20, 22, 92, 23, 85, 89, 68, 68, 89, 11, 71, 89, 27, 9, 83, 84, 93, 1, 57, 42, 83, 7, 13, 96, 69, 29, 86, 81, 52, 4, 7, 64, 70]
text = ""
for i in range(len(enc)):
    text += char(enc[i] ^ key[i % len(key)])
```
"""

def main():
    KEY = [119, 104, 52, 116, 52, 114, 51, 121, 48, 117, 100, 48, 49, 110, 103, 63]
    ENC = [32, 13, 88, 24, 20, 22, 92, 23, 85, 89, 68, 68, 89, 11, 71, 89, 27, 9, 83, 84, 93, 1, 57, 42, 83, 7, 13, 96, 69, 29, 86, 81, 52, 4, 7, 64, 70]

    KEY_LEN = len(KEY)
    ENC_LEN = len(ENC)

    text = ""

    for i in range(len(ENC)):
        text += chr(ENC[i] ^ KEY[i % KEY_LEN])
    
    print(text)

if __name__ == "__main__":
    main()

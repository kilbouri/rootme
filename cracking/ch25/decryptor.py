CIPHER_KEY_HEX: str = "18 D6 15 CA FA 77 00"
CIPHER_TEXT_HEX: str =  "50 B3 67 AF A5 0E 77 A3 4A A2 9B 01 7D 89 61 A5 A5 02 76 B2 70 B8 89 03 79 B8 71 95 9B 28 74 BF 61 BE 96 12 47 95 3E E1 A5 04 6C A3 73 AC 89 00"

def hex_string_to_bytes(hex_str: str):
    return tuple(map(lambda x: int(x, 16), hex_str.split(' ')))

def str_len(bytes: list[int]):
    l = 0
    while bytes[l] != 0:
        l += 1

    return l

def unpack(key_bytes: list[int], text_bytes: list[int]):
    ret_val = ""
    curr_index = 0

    while text_bytes[curr_index] != 0:
        curr_text = text_bytes[curr_index]
        curr_key = key_bytes[curr_index % str_len(key_bytes)]

        ret_val += chr(curr_text ^ curr_key)
        curr_index += 1

    return ret_val


def main():
    key_bytes = hex_string_to_bytes(CIPHER_KEY_HEX)
    text_bytes = hex_string_to_bytes(CIPHER_TEXT_HEX)

    print("inputs:")
    print(f"  {CIPHER_KEY_HEX=} ({key_bytes})")
    print(f"  {CIPHER_TEXT_HEX=} ({text_bytes})")

    print("output:")
    print(f"  {unpack(key_bytes, text_bytes)}")

if __name__ == "__main__":
    main()

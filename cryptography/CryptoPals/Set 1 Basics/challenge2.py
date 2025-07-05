"""
Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:
1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:
686974207468652062756c6c277320657965

... should produce:
746865206b696420646f6e277420706c6179
"""


def main():
    # Take 2 user input strings
    string_1 = input("Enter string 1: ")
    string_2 = input("Enter string 2: ")

    # Check if strings are of equal length
    if len(string_1) == len(string_2):
    # Convert hex strings to bytes
        string_1_to_bytes = bytes.fromhex(string_1)
        string_2_to_bytes = bytes.fromhex(string_2)

        result = []

        # XOR each byte of the two inputs
        for i in range(len(string_1_to_bytes)):
            xor = string_1_to_bytes[i] ^ string_2_to_bytes[i]
            result.append(xor)

        # Convert XOR result to hex and print
        for j in range(len(result)):
            result_in_hex = format(result[j], '02x')  # Convert int to 2-digit hex
            print(result_in_hex, end="")

        print("")
    else:
        print("Error: Strings must be of equal length")

main()

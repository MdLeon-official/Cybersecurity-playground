"""
Single-byte XOR cipher

The hex encoded string:
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.
You can do this by hand. But don't: write code to do it for you.
How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric.
Evaluate each output and choose the one with the best score.
"""

# Hex string to raw bytes
def hex_to_bytes(str):
    return bytes.fromhex(str)

# English Score check
def english_score(text):
    frequency = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3,
        'e': 12.7, 'f': 2.2, 'g': 2.0, 'h': 6.1,
        'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0,
        'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9,
        'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1,
        'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15,
        'y': 2.0, 'z': 0.074, ' ': 13.0
    }

    score = 0
    for char in text.lower():
        score += frequency.get(char, -5)  # Penalize unknown characters with -5
    return score


def main():
    hex_stirng = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


    h_to_b = hex_to_bytes(hex_stirng)
    # eng_score = english_score("hello world")
    #print(h_to_b)
    # print(eng_score)
    total_result = []
    keys = []
    plaintext_Arr = []
    score_Arr = []
    for key in range(256):
        try:
            xored = bytes([b ^ key for b in h_to_b])
            plaintext = xored.decode('utf-8')
            score = english_score(plaintext)

            keys.append(key)
            plaintext_Arr.append(plaintext)
            score_Arr.append(score)
            total_result.append({
                "key": key,
                "score": score,
                "plaintext": plaintext
            })
        except UnicodeDecodeError:
            continue

    max_score = max(score_Arr)
    # for result in total_result:
    #     print(result)
    for result in total_result:
        if result["score"] == max_score:
            print(f"Plaintext: {result["plaintext"]}")
            print(f"Score: {result["score"]}")
            print(f"Key: {result["key"]}")

main()

"""http://projecteuler.net/problem=059

XOR decryption

Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using cipher1.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 107359

FILENAME = 'cipher1.txt'

def get_cipher_bytes():
    cipher = None
    with open(FILENAME) as f:
        cipher = f.read()
        f.close()
    cipher_bytes = [int(c) for c in cipher.split(',')]
    return cipher_bytes

def get_passwords_iterator():
    pw_start = ord('a')
    pw_end = ord('z')
    for a in xrange(pw_start, pw_end + 1):
        for b in xrange(pw_start, pw_end + 1):
            for c in xrange(pw_start, pw_end + 1):
                yield [a, b, c,]

def decrypt_cipher(cipher_bytes, key):
    message_bytes = []
    key_length = len(key)
    ascii_printable_start = ord(' ') # 32 / 0x20
    ascii_printable_end = ord('~') # 126 / 0x7E
    for i in xrange(len(cipher_bytes)):
        o = cipher_bytes[i] ^ key[i % key_length]
        if ascii_printable_start <= o <= ascii_printable_end:
            c = chr(o)
            message_bytes.append(c)
        else:
        #print chr(o), o
            # cannot be a valid decrypted message if it contains non-printable ASCII
            message_bytes = None
            break
    return message_bytes

def solve():
    """
    The major helpful clue is that the password is 3 lower-case ASCII characters--
    This gives us 26**3 = 17576 possible passwords, quite easy to brute force.

    Technique:
    The most common character in a language, assuming spaces aren't stripped out, is the space character.
    https://en.wikipedia.org/wiki/Frequency_analysis

    $ time python 059.py
    (The Gospel of John, chapter 1) 1 In the beginning the Word already existed. He was with God, and he was God. 2 He was in the beginning with God. 3 He created everything there is. Nothing exists that he didn't make. 4 Life itself was in him, and this life gives light to everyone. 5 The light shines through the darkness, and the darkness can never extinguish it. 6 God sent John the Baptist 7 to tell everyone about the light so that everyone might believe because of his testimony. 8 John himself was not the light; he was only a witness to the light. 9 The one who is the true light, who gives light to everyone, was going to come into the world. 10 But although the world was made through him, the world didn't recognize him when he came. 11 Even in his own land and among his own people, he was not accepted. 12 But to all who believed him and accepted him, he gave the right to become children of God. 13 They are reborn! This is not a physical birth resulting from human passion or plan, this rebirth comes from God.14 So the Word became human and lived here on earth among us. He was full of unfailing love and faithfulness. And we have seen his glory, the glory of the only Son of the Father.
    Expected: 107359, Answer: 107359

    real0m0.824s
    user0m0.796s
    sys0m0.015s
    """
    cipher_bytes = get_cipher_bytes()
    best_so_far = 0
    message = None
    for password in get_passwords_iterator():
        possible_message = decrypt_cipher(cipher_bytes, password)
        if possible_message:
            num_spaces = len(filter(lambda x: x == ' ', possible_message))
            if num_spaces >= best_so_far:
                best_so_far = num_spaces
                message = possible_message
    print ''.join(message)
    answer = sum([ord(c) for c in message])
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

# coding=utf-8

def main():
    key_space = "abcdefghijklmnopqrstuvwxyzåäö ,."
    #key_space = "abcdefghijklmnopqrstuvwxyz"
    key = "summer"

    f = open("sample.txt", "r+")
    plain = f.read()
    plain = sanitize(plain.lower(), key_space)
    f.seek(0)
    f.truncate()
    f.write(plain)
    f.close()

    cipher = encrypt(plain, key_space, key)

    f = open("encryption.txt", "w+")
    f.write(cipher)
    f.close()

    decrypt(cipher, key_space, key)

def encrypt(plain, key_space, key):
    K = len(key_space)
    key_length = len(key)
    cipher = ""

    i = 0
    for char in plain:
        if key_space.find(char) >= 0:
            """
            Adds the character value from the key to the plaintext character, divides it by the amount of characters
            in the key_space, and calculates the remainder. This ensures that it will always wrap around and start from
            0, keeping the index within the key_space.
            plaintext character value + key character value modulo K
            """
            cipher_index = (key_space.index(char) + key_space.index(key[i])) % K
            cipher += key_space[cipher_index]
            i += 1
            if i == key_length: i = 0
        else:
            print("Encountered character not in key_space, character will be left as plaintext")
            cipher = cipher + char # Note, cipher key does not advance

    print("Encrypted text:", cipher)
    return cipher

def decrypt(cipher, key_space, key):
    K = len(key_space)
    key_length = len(key)
    plain = ""

    i = 0
    for char in cipher:
        if key_space.find(char) >= 0:
            # Since python allows indexing of string with negative numbers, this will automatically wrap around from 0 to K
            plain_index = key_space.index(char) - key_space.index(key[i])
            plain += key_space[plain_index]
            i += 1
            if i == key_length: i = 0
        else:
            print("Encountered character not in key_space, character will not be decrypted")
            plain = plain + char # Note, cipher key does not advance

    print("Decrypted text:", plain)
    return plain

def sanitize(text, key_space):
    for char in text:
        if key_space.find(char) >= 0:
            continue
        else:
            text = text.replace(char, "")
    return text

if __name__ == '__main__':
    main()

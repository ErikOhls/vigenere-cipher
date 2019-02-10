# coding=utf-8

import time as t
import sys

def main():
    key_space = "abcdefghijklmnopqrstuvwxyzåäö ,."

    # Finds key and decrypts for all groups, prints decrypted texts and a timetable
    test_all = True
    if test_all:
        start_total = t.time()
        time_array = []
        key_array = []
        plain_array = []
        # Open files and decrypt
        for i in range(1,20):
            file_name = "vig_group" + str(i) + ".crypto"
            try:
                f = open(file_name, "r")
            except IOError:
                print("Can't open file")
                sys.exit()
            cipher = f.read()
            f.close
            cipher = sanitize(cipher, key_space)

            start = t.time()
            key_length = find_key_length_coin(cipher)
            key = find_key_chi(cipher, key_length, key_space)
            plain = decrypt(cipher, key_space, key)
            end = t.time()
            time_array.append(end-start)
            key_array.append(key)
            plain_array.append(plain)

        # Calculate times
        end_total = t.time()
        total = end_total - start_total
        total = round(total, 5)
        avarage = total / 18
        avarage = round(avarage, 5)

        # Print plaintexts
        for i in range(0,19):
            print("Group " + str(i+1) + ":\nKey: " + key_array[i])
            print("Plaintext:\n", plain_array[i], "\n\n")

        # Format time table
        timetable = "{:^20}".format("TIMETABLE") + "\n"
        timetable += "--------------------\n"
        for i in range(0,19):
            time = round(time_array[i], 5)
            timetable += "{:>10}".format("Group " + str(i+1) + ":")
            timetable += "{:<10}".format("  " + str(time) + "s\n")
        timetable += "--------------------\n"
        timetable += "{:>10}".format("Total:")
        timetable += "{:<10}".format("  " + str(total) + "s\n")
        timetable += "{:>10}".format("Avarage:")
        timetable += "{:<10}".format("  " + str(avarage) + "s\n")
        print(timetable)

    # Finds key and decrypts for one cipher
    test_single = False
    if test_single:
        file_name = "text1.crypto"
        try:
            f = open(file_name, "r")
        except IOError:
            print("Can't open file")
            sys.exit()
        cipher = f.read()
        f.close
        cipher = sanitize(cipher, key_space)

        start = t.time()
        key_length = find_key_length_coin(cipher)
        key = find_key_chi(cipher, key_length, key_space)
        plain = decrypt(cipher, key_space, key)
        end = t.time()
        total = end - start

        print("Key length:", key_length, "key:", key, "Plaintext:\n", plain, "\nTime taken", total)

def find_key_length_coin(cipher):
    """
    Sig:    string ==> int
    Pre:    cipher is a vigenere cipher
    Post:   integer corresponding to possible key length used to encrypt cipher

    Example: Let cipher be a string consisting of a vigenere cipher text
             find_key_length_coin(<cipher>) ==> 16
    """
    cipher_length = len(cipher)
    coincidence_array = []
    start_length = 3
    #stop_length = round(len(cipher) / 20) # This was used when trying ciphers not provided by other groups
    stop_length = 18

    # Try these key lengths, and add to coincidence_array for comparison
    for i in range(start_length, stop_length):
        grouped_array = group_cipher(cipher, i)
        total = 0

        # Find coincidence index for all groups of text
        for text in grouped_array:
            occurance = {}
            # Find total occurances
            for char in text:
                if char in occurance:
                    occurance[char] += 1
                else: occurance[char] = 1

            # Executes formula for coincidence index
            for char in occurance:
                occurance[char] = occurance[char] * (occurance[char] - 1)
            summation = sum(occurance.values())
            coincidence = summation / (cipher_length * (cipher_length - 1))

            total += coincidence

        coincidence_array.append(total)

    i = start_length
    key_length = i

    # Find a jump in coincidence value, indicating key length
    for value in coincidence_array:
        if value == coincidence_array[0]: # Round one
            max_value = value
            prev_value = value
            i += 1
            continue

        # A jump of value around 1.4 times the previous value seems like the most accurate indication\
        # that the key length has been found
        if value > prev_value * 1.4:
            max_value = value
            key_length = i
        i += 1
        prev_value = value

    return key_length

def find_key_chi(cipher, key_length, key_space):
    """
    Sig:    string, int, string ==> string
    Pre:    cipher is a string of characters encrypted by the vigenere cipher, key_length < length of cipher,\
            key_space contains all types of characters in cipher
    Post:   String possibly being the key the cipher was encrypted with

    Example: Let cipher be a string encrypted by the vigenere cipher. Key_length the correct length of key \
             used to encrypt text with, and key_space containing all types of characters contained in cipher
             find_key_chi(<cipher>, 5, abcdefghijklmnopqrstuvwxyzåäö ,.) ==> a key
             find_key_chi(<cipher>, 10, abcdefghijklmnopqrstuvwxyzåäö ,.) ==> djfueo,åso
    """
    group_array = group_cipher(cipher, key_length)

    key = ""
    for text in group_array:
        chi_array = []
        # This is essentially the same as cracking a Ceasar cipher.
        # Finds chi-squared for all possible shifts of the cipher for each particular letter of the key
        for i in range(len(key_space)):
            chi_total = get_chi_value(text, key_space)
            chi_array.append(chi_total)

            # Shift all of the text one space to the left in the key space. b ==> a, ö ==> ä, etc
            shift = ""
            for char in text:
                char_index = key_space.index(char) - 1
                shift += key_space[char_index]

            text = shift

        # The amount needed to shift is the same amount as the minimal chi value for this group of characters
        index_value = min(chi_array)
        shift_amount = chi_array.index(index_value)

        letter = key_space[shift_amount]
        key += letter

    return key

def get_chi_value(text, key_space):
    """
    Sig:    string, string ==> float
    Pre:    text is a string, key_space contains all types of character in string text
    Post:   float with value corresponding to the similarity between the occurances of characters in the text,\
            and the occurances between characters in a text writting in Swedish

    Example: let key_space contain all types characters in text
             get_chi_value(<Swedish text>, <key_space>) ==> 54.1545
             get_chi_value(<English text>, <key_space>) ==> 1457.356
    """
    swe_probability = [0.0938, 0.0154, 0.0149, 0.047, 0.1015, 0.0203, 0.0286, 0.0209, 0.0582, 0.0064, 0.0314, 0.0528, 0.0347, 0.0853, \
                       0.0448, 0.0184, 0.0002, 0.0873, 0.0659, 0.0769, 0.0192, 0.0242, 0.0014, 0.0016, 0.007, 0.0007, 0.0134, 0.018, 0.0131, 0.1, 0.007, 0.015]

    # Count occurances of characters
    occurance_tmp = {}
    for char in key_space:
        occurance_tmp[char] = 0
    for char in text:
        if char in occurance_tmp:
            occurance_tmp[char] +=1

    occurance_array = list(occurance_tmp.values())

    # Calculate chi squared
    chi_total = 0
    for char in text:
        char_index = key_space.index(char)
        expected = len(text) * swe_probability[char_index]
        chi = (occurance_array[char_index] - expected) * (occurance_array[char_index] - expected) / expected
        chi_total += chi

    return chi_total

def group_cipher(cipher, key_length):
    """
    Sig:    string, int ==> string[0..key_length]
    Pre:    cipher is a string, key_length value is shorter than the value of the length of cipher
    Post:   array containing strings, with every string being the n'th character in the string, and n being the key_length

    Example:
             group_cipher(abcdef, 3) ==> ["ad", "be", "cf"]
             group_cipher(abcdef, 2) ==> ["ace", "bdf"]
    """
    group_array = []
    group = ""
    i = 0

    for j in range(0, key_length):
        i = j
        while i < len(cipher):
            group += (cipher[i:i+1])
            i += key_length

        group_array.append(group)
        group = ""

    return group_array

def decrypt(cipher, key_space, key):
    """
    Sig:    string, string, string ==> string
    Pre:    cipher is a vigenere cipher, key_space contains all types of characters in cipher, key is the key \
            used to encrypt plaintext with
    Post:   plaintext of cipher
    """
    K = len(key_space)
    key_length = len(key)
    plain = ""

    i = 0
    for char in cipher:
        if key_space.find(char) >= 0:
            plain_index = key_space.index(char) - key_space.index(key[i])
            plain += key_space[plain_index]
            i += 1
            if i == key_length: i = 0
        else:
            print("Encountered character not in key_space, character will not be decrypted")
            plain = plain + char # Note, cipher key does not advance

    return plain

def sanitize(text, key_space):
    """
    Sig:    string, string ==> string
    Pre:    None
    Post:   string of text with any characters not contained in key_space not in text

    Example:
             sanitize(abc, ab) ==> ab
             sanitize(abcdfgab, ab) ==> abab
    """
    for char in text:
        if key_space.find(char) >= 0:
            continue
        else:
            text = text.replace(char, "")
    return text

""" -------------------------------------------------------------------------------- """
""" --------- Below this line is code unused for decrypting studen ciphers --------- """
""" -------------------------------------------------------------------------------- """

def find_key_length_friedman(cipher, n):
    # This is left for posterity. It is an attempt at implementing a version of the friedman test.
    # Unfortunately it does not return any meaningful values
    occurance = {}
    cipher_length = len(cipher)

    ES = 0.0681
    k = len(cipher)

    for char in cipher:
        if char in occurance:
            occurance[char] += 1
        else: occurance[char] = 1

    for char in occurance:
        occurance[char] = occurance[char] * (occurance[char] - 1)

    total = sum(occurance.values())
    coin_index = total / (cipher_length * (cipher_length-1))
    T = coin_index

    top = ( ES - ( 1 / n ) ) * k
    first = ( k - 1 ) * T
    second = k * (1 / n ) + ES

    result = top / (first - second)

    return result

def find_key_length_kasisky(cipher):
    """
    Sig:    string ==> int
    Pre:    cipher is a vigenere cipher
    Post:   integer corresponding to possible key length used to encrypt cipher

    Example: Let cipher be a string consisting of a vigenere cipher text
             find_key_length_kasisky(<cipher>) ==> 16
    """
    distance_array = get_distance_array(cipher)
    key_length = 0
    max_occurance = 0
    occurance = 0
    stop_length = round(len(cipher) / 20)

    # Counts how many times a number evenly divides distances between repeating sets of characters
    for i in range(2, stop_length):
        for distance in distance_array:
            if distance % i == 0:
                occurance += 1

        # Check if current number is larger than previous
        #print(i, occurance, max_occurance)
        if occurance > max_occurance:
            max_occurance = occurance
            key_length = i

        # This is needed because, e.g. anything divisible by 4, will also be divisible by 2.
        # Resulting in smaller numbers always taking precedence over bigger ones
        elif i % key_length == 0 and occurance > max_occurance * 0.9:
            max_occurance = occurance
            key_length = i

        occurance = 0

    return key_length

def get_distance_array(cipher):
    """
    Sig:    string ==> int[0..|nr instances of recurring sets of 3 characters|]
    Pre:    cipher is a string of characters
    Post:   Array with integers, each integer representing the dinstance between a set of 3 characters found\
            later in the string

    Example: Let cipher be a string
             get_distance_array(abcabc) ==> [3]
             get_distance_array(aaabbbaaapppbbb) = [6, 9]
    """
    distance_array = []
    start_value = 0
    distance = 0

    # For every character...
    for char in cipher:
        i = start_value
        j = start_value+3

        # ...compare the following 3 characters with the rest of the string
        for x in range(i, len(cipher)):
            if cipher[start_value:start_value+3] == cipher[i:j] and distance != 0:
                distance_array.append(distance)
                distance = 0
            i += 1
            j += 1
            distance += 1

        start_value += 1
        distance = 0

    return distance_array

if __name__ == '__main__':
    main()

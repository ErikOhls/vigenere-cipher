# coding=utf-8

def main():
    key_space = "abcdefghijklmnopqrstuvwxyzåäö ,."
    #key_space = "abcdefghijklmnopqrstuvwxyz"

    f = open("encryption.txt", "r")
    cipher = f.read()
    f.close()
    #print(cipher)

    key_length = find_key_length(cipher)
    key = find_key(cipher, key_length, key_space)

def find_key_length(cipher):
    distance_array = get_distance_array(cipher)
    key_length = 0
    max_occurance = 0
    occurance = 0

    # Finds the most common number which evenly divides all numbers in the array
    print("i, occurance, max occurance")
    for i in range(2, 9):
        for distance in distance_array:
            if distance % i == 0:
                occurance += 1

        print(i, occurance, max_occurance)
        if occurance > max_occurance:
            max_occurance = occurance
            key_length = i

        # This is needed because, e.g. anything divisible by 4, will also be divisible by 2.
        # Resulting in smaller numbers always taking precedence over bigger ones
        elif i % key_length == 0 and occurance > max_occurance * 0.9:
            max_occurance = occurance
            key_length = i

        occurance = 0

    print("key length is:", key_length)

    return key_length

def get_distance_array(cipher):
    # Gets distances of recurring groups of 3 characters.
    # abcabc = [3], aaabbbaaapppbbb = [6, 9]
    distance_array = []
    start_value = 0
    distance = 0

    # For every character...
    for char in cipher:
        i = start_value
        j = start_value+3
        if i % 100 == 0: print("loop:", i, "out of:", len(cipher))

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

def find_key(cipher, key_length, key_space):
    group_array = group_cipher(cipher, key_length)
    most_common_array = []
    key = ""

    # Count occurances of each letter, in each group
    for group in group_array:
        occurance = {}
        for char in group:
            if char in occurance:
                occurance[char] += 1
            else: occurance[char] = 1

        most_common = max(occurance, key=occurance.get)
        most_common_array.append(most_common)

    print(most_common_array)

    # Shift letters to find key
    for char in most_common_array:
        current_index = key_space.index(char)
        # Why is it always 3??????
        new_index = (current_index + 3) % len(key_space)

        key += key_space[new_index]

    print("Key is:", key)

    return key

def group_cipher(cipher, key_length):
    # Groups characters according to key length
    # group_cipher("abcdef", 3) = ["ad", "be", "cf"]
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

if __name__ == '__main__':
    main()

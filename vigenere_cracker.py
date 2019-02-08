# coding=utf-8
import vigenere as vig

def main():
    key_space = "abcdefghijklmnopqrstuvwxyzåäö ,."

    f = open("vig_group2.crypto", "r")
    cipher = f.read()
    f.close()
    cipher = vig.sanitize(cipher, key_space)

    test_all = True
    if test_all:
        for i in range(1,19):
            file_name = "vig_group" + str(i) + ".crypto"
            f = open(file_name, "r")
            cipher = f.read()
            f.close

            key_length_fried =find_key_length_friedman(cipher)
            key_length = find_key_length(cipher)
            simple = find_key_length_simple(cipher, len(key_space))

            print("group", i, "Friedman", key_length_fried, "= kasisky", key_length, "?", "simple:", simple)

    test_big = False
    if test_big:
        for i in range(1,19):
            file_name = "vig_group" + str(i) + ".crypto"
            f = open(file_name, "r")
            cipher = f.read()
            f.close
            cipher = vig.sanitize(cipher, key_space)

            key_length = find_key_length(cipher)
            key = find_key_chi(cipher, key_length, key_space)
            plain = vig.decrypt(cipher, key_space, key)
            validity = get_chi_value(plain, key_space)
            print("Group:", i, "Validity:", validity)

    test_other = False
    if test_other:
        for i in range(4, 5):
            file_name = "text" + str(i) + ".crypto"
            f = open(file_name, "r")
            cipher = f.read()
            f.close
            cipher = vig.sanitize(cipher, key_space)

            key_length = find_key_length_friedman(cipher)
            find_key_length(cipher)
            key = find_key_chi(cipher, key_length, key_space)
            plain = vig.decrypt(cipher, key_space, key)
            simple = find_key_length_simple(cipher, len(key_space))
            print("Group:", i, simple)
            print(plain)

    test_brute = False
    if test_brute:
        file_name = "text2.crypto"
        f = open(file_name, "r")
        cipher = f.read()
        f.close
        cipher = vig.sanitize(cipher, key_space)

        for i in range(1, 50):
            key = find_key_chi(cipher, i, key_space)
            plain = vig.decrypt(cipher, key_space, key)
            print("Group:", i)
            print(plain)

def find_key_length_simple(cipher, n):
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


def find_key_length_friedman(cipher):
    length = len(cipher)
    coincidence_array = []
    co_dict = {}
    start_length = 3
    stop_length = round(len(cipher) / 20)

    # Try these key lengths
    for i in range(start_length, stop_length):
        grouped_array = group_cipher(cipher, i)
        total = 0

        # Find total occurances
        for text in grouped_array:
            sub_total = 0
            occurance = {}
            for char in text:
                if char in occurance:
                    occurance[char] += 1
                else: occurance[char] = 1

            # Sum c1(c1-1)
            for char in occurance:
                occurance[char] = occurance[char] * (occurance[char] - 1)

            sub_total = sum(occurance.values())
            coincidence = sub_total / (length * (length - 1))
            total += coincidence
        coincidence_array.append(total)
        co_dict[i] = total
    #print(co_dict)

    i = start_length
    key_length = i

    # Find maximum(relative, sort of) index of coincidence
    for value in coincidence_array:
        if value == coincidence_array[0]:
            max_value = value
            prev_value = value
            i += 1
            continue

        print("key", i, "Current max:", max_value, "Current value:", value)

        if value  > prev_value * 1.3:
            max_value = value
            key_length = i
        i += 1
        prev_value = value

    #print("key length is:", key_length)
    return key_length

def find_key_length(cipher):
    distance_array = get_distance_array(cipher)
    key_length = 0
    max_occurance = 0
    occurance = 0
    stop_length = round(len(cipher) / 20)

    # Counts how many times a number evenly divides distances between repeating sets of characters
    print("i, occurance, max occurance")
    for i in range(2, stop_length):
        for distance in distance_array:
            if distance % i == 0:
                occurance += 1

        # Check if current number is larger than previous
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

    #print("key length is:", key_length)

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
        #if i % 100 == 0: print("loop:", i, "out of:", len(cipher))

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

def find_key_chi(cipher, key_length, key_space):
    swe_probability = [0.0938, 0.0154, 0.0149, 0.047, 0.1015, 0.0203, 0.0286, 0.0209, 0.0582, 0.0064, 0.0314, 0.0528, 0.0347, 0.0853, \
                       0.0448, 0.0184, 0.0002, 0.0873, 0.0659, 0.0769, 0.0192, 0.0242, 0.0014, 0.0016, 0.007, 0.0007, 0.0134, 0.018, 0.0131, 0.1, 0.007, 0.015]
    group_array = group_cipher(cipher, key_length)

    key = ""
    for text in group_array:
        chi_array = []
        for i in range(len(key_space)):
            chi_total = get_chi_value(text, key_space)
            chi_array.append(chi_total)

            shift = ""
            for char in text:
                char_index = key_space.index(char) - 1
                shift += key_space[char_index]

            text = shift

        index_value = min(chi_array)
        shift_amount = chi_array.index(index_value)

        letter = key_space[shift_amount]
        #print(letter, shift_amount)
        key += letter

    print("key is:", key)
    return key

def get_chi_value(text, key_space):
        swe_probability = [0.0938, 0.0154, 0.0149, 0.047, 0.1015, 0.0203, 0.0286, 0.0209, 0.0582, 0.0064, 0.0314, 0.0528, 0.0347, 0.0853, \
                       0.0448, 0.0184, 0.0002, 0.0873, 0.0659, 0.0769, 0.0192, 0.0242, 0.0014, 0.0016, 0.007, 0.0007, 0.0134, 0.018, 0.0131, 0.1, 0.007, 0.015]

        occurance_tmp = {}
        for char in key_space:
            occurance_tmp[char] = 0
        for char in text:
            if char in occurance_tmp:
                occurance_tmp[char] +=1

        occurance_array = list(occurance_tmp.values())

        chi_total = 0
        for char in text:
            char_index = key_space.index(char)
            expected = len(text) * swe_probability[char_index]
            chi = (occurance_array[char_index] - expected) * (occurance_array[char_index] - expected) / expected
            chi_total += chi

        return chi_total

def check_validity(text, key_space):
        swe_probability = [0.0938, 0.0154, 0.0149, 0.047, 0.1015, 0.0203, 0.0286, 0.0209, 0.0582, 0.0064, 0.0314, 0.0528, 0.0347, 0.0853, \
                       0.0448, 0.0184, 0.0002, 0.0873, 0.0659, 0.0769, 0.0192, 0.0242, 0.0014, 0.0016, 0.007, 0.0007, 0.0134, 0.018, 0.0131, 0.1, 0.007, 0.015]

        occurance_tmp = {}
        for char in key_space:
            occurance_tmp[char] = 0
        for char in text:
            if char in occurance_tmp:
                occurance_tmp[char] +=1

        occurance_tmp = list(occurance_tmp.values())
        total = sum(occurance_tmp)
        occurance_array = []
        for value in occurance_tmp:
            relative_value = (value / total) * 100
            occurance_array.append(relative_value)

        chi_total = 0
        for char in text:
            char_index = key_space.index(char)
            expected = len(text) * swe_probability[char_index]
            chi = (occurance_array[char_index] - expected) * (occurance_array[char_index] - expected) / expected
            chi_total += chi

        return chi_total

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

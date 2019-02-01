# coding=utf-8

def main():
    key_space = "abcdefghijklmnopqrstuvwxyzåäö ,."
    key = "key"

    f = open("dirty.txt", "r")
    text = f.read()
    f.close()

    print(text)

    text = sanitize(text, key_space)

    f = open("sample.txt", "w+")
    f.write(text)
    f.close()

def sanitize(text, key_space):
    for char in text:
        if key_space.find(char) >= 0:
            continue
        else:
            text = text.replace(char, "")
    return text

if __name__ == '__main__':
    main()

"""This takes the already modified CEDICT and removes spaces between the
pinyin"""

def main():
    with open("cedict_modified.txt", "r") as ce:
        with open("text.txt", "w") as te:
            for line in ce:
                line1 = line.rstrip('/')
                pinyin = line1.split('/')[0].split('[')[1].rstrip(' ]')
                pinyin_no_space = pinyin.replace(' ', '')
                line = line.replace(pinyin, pinyin_no_space)

                te.write(line)


if __name__ == "__main__":
    main()

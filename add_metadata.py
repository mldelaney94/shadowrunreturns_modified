""" This program takes in a language translation (LT) in PO format, and the original
english language POT (ELP) file (strings.pot), and sorts the LT in the same
order as the ELP. This ensures that later language analysis can be done with some
level of correctness wrt the order of the conversations the player will have.

For instance, if we want to know if the player has seen a word before, we need
to know everything the player has seen until now. This would be nice to create
an addon for in game, but unfortunately that would be a lot more work."""

import sys
import os
import re
import jieba

from materials.cc_cedict_materials import cc_cedict_parser

ELP = 'translations\\en\\Strings.pot'

def add_pinyin_to_chinese_strings():
    word_list = []
    jieba.set_dictionary('materials/dicts/jieba_dict_large.txt')
    cc_cedict_parser.QUIET = True
    zh_dict = cc_cedict_parser.parse_dict('simp')
    with open('translations\\cn\\deadmanswitchcn.po', 'r') as f:
        for line in f:
            word_list = list(jieba.cut(line, cut_all=False))

#TODO change cc_cedict_parser to use dictionaries for ease of reading over
#this current thing of using digits







def make_comments_human_readable():
    """The ELP has many comments that contain hashstrings. These hashstrings
    correspond to a file in the 'convos' folder. Those files contain a human
    readable short description. This function replaces all hashstrings in the
    ELP with that description."""

    #(hashcode, metadata) tuples
    hashcode_metadata_tuples = pair_hashcodes_and_metadata()
    with open(ELP, 'r') as f:
        newText = f.read()

    for grouple in hashcode_metadata_tuples:
        newText = newText.replace(grouple[0], grouple[1])

    with open(ELP, 'w') as f:
        f.write(newText)


def pair_hashcodes_and_metadata():
    """ pairs hashcodes with their corresponding descriptive data """
    hashcode_metadata_tuples = []
    for filename in os.listdir('convos'):
        #get hashcode from file name
        hashcode = bytes(filename.split('.')[0], 'utf-8')

        filepath = 'convos\\' + filename #os.listdir does not return a path
        with open(filepath, 'rb') as curr_file:
            #because files in convo folder are bytes files, time is spent
            #decoding them to strings
            for line in curr_file:
                if hashcode in line:
                    description_text = re.search(b'(c\d\d-.+)\x1a', line)
                    #approximately 10-20 lines will have to be replaced
                    #manually as this regex doesn't cover them
                    if description_text != None:
                        decoded_desc_text = description_text.group(1).decode("utf-8", "ignore")
                        string_hashcode = str(hashcode).split('\'')[1]
                        hashcode_metadata_tuples.append((string_hashcode, decoded_desc_text))
                    break

    return hashcode_metadata_tuples

if __name__ == "__main__":
    add_pinyin_to_chinese_strings()

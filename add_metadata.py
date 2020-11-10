""" This program takes in a language translation (LT) in PO format, and the original
english language PO (ELP) file (strings.po), and sorts the LT in the same
order as the ELP. This ensures that later language analysis can be done with some
level of correctness wrt the order of the conversations the player will have.

For instance, if we want to know if the player has seen a word before, we need
to know everything the player has seen until now. This would be nice to create
an addon for in game, but unfortunately that would be a lot more work."""

import sys
import os
import re

ELP = 'translations\\en\\Strings.pot'

def main(LT):
    en = open(ELP, 'r')
    lt = open(LT, 'r')
    dump = open("text.po", "w")

def make_comments_human_readable():
    """The ELP has many comments that contain hashstrings. These hashstrings
    correspond to a file in the 'convos' folder. Those files contain a human
    readable short description. This function replaces all hashstrings in the
    ELP with that description."""

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

def replace_hashcode_in_ELP(hashcode, replacement):
    with open(ELP) as f:
        newText = f.read().replace(hashcode, replacement)
    
    with open(ELP, 'w') as f:
        f.write(newText)
            

if __name__ == "__main__":
   # if len(sys.argv) <= 1:
   #     print("Please input a PO language file")
   #     sys.exit(2)

   # LT = sys.argv[1]
   # main(LT)
   make_comments_human_readable()

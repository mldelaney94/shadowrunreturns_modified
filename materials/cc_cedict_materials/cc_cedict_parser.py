""" A parser for the CC-Cedict. Convert the Chinese-English dictionary into a 
list of python dictionaries with "traditional","simplified", "pinyin",
and "english" keys.

Make sure that the cedict_ts.u8 file is in the same folder as this file,
and that the name matches the file name on line 13.

Before starting, open the CEDICT text file and delete the copyright 
information at the top. Otherwise the program will try to parse it and you
will get an error message.

Characters that are commonly used as surnames have two entries in CC-CEDICT.

This code was written by Franki Allegra in February 2020. Edited by Matthew Delaney February 2020
https://github.com/rubber-duck-dragon/rubber-duck-dragon.github.io/blob/master/cc-cedict_parser/parser.py
"""


import sys
from pathlib import Path

#define functions

#builds a dictionary with a trad or simp character as the key
def parse_lines(lines, key_is_trad_or_simp):
    dictionary = {}
    for line in lines:
        if line == '':
            continue
        parts = get_parts_of_line(line)
        add_entry(parts, dictionary, key_is_trad_or_simp)
    
    return dictionary

def get_parts_of_line(line):
    parts = {}
    line = line.rstrip('/')
    line = line.split('/')
    
    parts['english'] = line[1:]
    
    pinyin_hanzi = line[0].split('[')
    hanzi = pinyin_hanzi[0]
    hanzi = hanzi.split(' ')
    parts['trad_hanzi'] = hanzi[0]
    parts['simp_hanzi'] = hanzi[1]
    
    pinyin = pinyin_hanzi[1]
    pinyin = pinyin.rstrip(' ]')
    parts['pinyin'] = pinyin
    
    return parts
    
#no return deliberately
def add_entry(parts, dictionary, key_is_trad_or_simp):
    if key_is_trad_or_simp == 'trad':
        key = parts['trad_hanzi']
        non_key = parts['simp_hanzi']
    else:
        key = parts['simp_hanzi']
        non_key = parts['trad_hanzi']

    pinyin = parts['pinyin']
    english = parts['english']
    attrib_list = []

    if key in dictionary:
        attrib_list = dictionary[key]
        for part in english:
            attrib_list.append(part)
        dictionary[key] = attrib_list
    else:
        attrib_list.append(non_key)
        attrib_list.append(pinyin)
        for part in english:
            attrib_list.append(part)
        dictionary[key] = attrib_list

def parse_dict(key_is_trad_or_simp):
    #make each line into a dictionary
    if not QUIET:
        print("Parsing dictionary . . .")
    with open(get_dict_path(), 'r') as f:
        text = f.read()
        lines = text.split('\n')
        dictionary = parse_lines(lines, key_is_trad_or_simp)
    if not QUIET:
        print("Done")

    return dictionary

def get_dict_path():
    """ This function assumes that the path of the dictionary is relatively set
    in stone """
    return Path("materials/dicts/cedict_modified.txt")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please type 'trad' or 'simp' as first argument depending on"
                " how you want the dictionary to be built.")
        exit()
    global QUIET
    QUIET = True
    parsed_dict = parse_dict(sys.argv[1])
    print(parsed_dict)

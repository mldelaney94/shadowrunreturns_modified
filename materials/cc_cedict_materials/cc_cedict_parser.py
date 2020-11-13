""" A parser for the CC-Cedict. Convert the Chinese-English dictionary into a 
list of python dictionaries with "traditional","simplified", "pinyin",
and "english" keys.

Make sure that the cedict_ts.u8 file is in the same folder as this file,
and that the name matches the file name on line 13.

Before starting, open the CEDICT text file and delete the copyright 
information at the top. Otherwise the program will try to parse it and you
will get an error message.

Characters that are commonly used as surnames have two entries in CC-CEDICT.
"""


import sys

#define functions

#builds a dictionary with a simp character as the key
#the key accesses a dictionary of attributes - pinyin, and english definition
#dictionary[key]['pinyin'] accesses a list
#dictionary[key]['english'] also accesses a list
def parse_lines(lines):
    dictionary = {}
    for line in lines:
        if line == '' or 'surname' in line:
            continue
        parts = get_parts_of_line(line)
        add_entry(parts, dictionary)
    
    return dictionary

def get_parts_of_line(line):
    parts = {}
    line = line.rstrip('/')
    line = line.split('/')
    
    parts['english'] = line[1:]
    
    pinyin_hanzi = line[0].split('[')
    hanzi = pinyin_hanzi[0]
    hanzi = hanzi.split(' ')
    parts['simp_hanzi'] = hanzi[1]
    
    pinyin = pinyin_hanzi[1]
    pinyin = pinyin.rstrip(' ]')
    parts['pinyin'] = pinyin
    
    return parts
    
#no return deliberately
def add_entry(parts, dictionary):
    key = parts['simp_hanzi']

    pinyin = parts['pinyin']
    english = parts['english']

    if key in dictionary:
        for part in english:
            dictionary[key]['english'].append(part)
    else:
        dictionary[key] = {} 
        dictionary[key]['pinyin'] = pinyin
        dictionary[key]['english'] = english

def parse_dict(path):
    #make each line into a dictionary
    with open(path, 'r') as f:
        text = f.read()
        lines = text.split('\n')
        dictionary = parse_lines(lines)

    return dictionary

if __name__ == "__main__":
    parsed_dict = parse_dict()
    print(parsed_dict)

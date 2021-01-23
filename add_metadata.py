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
    jieba.set_dictionary('materials/dicts/jieba_dict_large.txt')
    zh_dict = cc_cedict_parser.parse_dict('materials/dicts/cedict_modified.txt')

    g = open("test.po", "w")
    with open('materials\\translations\\cn\\deadmanswitchcn.po', 'r') as f:
        while (line := f.readline()):
            pinyin_list = []
            paragraph = []
            word_list = []
            if 'msgstr ""' in line: #lots of missing lines of this type
                g.write(line)
                while (line := f.readline()) != '\n': #load paragraph
                    g.write(line)
                    paragraph.append(line)
                g.write("\"\\n\"\n")
                g.write("\"\\n\"\n")
                for sentence in paragraph:
                    word_list.append(list(jieba.cut(sentence, cut_all=False)))
                pinyin_list.append(get_pinyin_from_characters(zh_dict,
                        word_list))
                g.write(format_pinyin_into_paragraphs(pinyin_list))
                g.write('\n')
            elif 'msgstr "' in line:
                g.write(line)
                paragraph.append(line)
                for sentence in paragraph:
                    word_list.append(list(jieba.cut(sentence, cut_all=False)))
                pinyin_list.append(get_pinyin_from_characters(zh_dict,
                        word_list))
                g.write(format_pinyin_into_paragraphs(pinyin_list))
            else:
                g.write(line)

    g.close()
                
def get_pinyin_from_characters(zh_dict, list_of_sents):
    """ assumes a list of a list of strings """
    pinyin = []
    for sentence in list_of_sents:
        for word in sentence:
            if word in zh_dict:
                pinyin.append(zh_dict[word]['pinyin'])
            else:
                for character in word:
                    if character < u'\u9fff' and character > u'\u4e00':
                        pinyin.append(zh_dict[character]['pinyin'])
                    else:
                        pinyin.append(character)

    return pinyin

def format_pinyin_into_paragraphs(pinyin_strings):
    """ assumes one list of lists of strings """
    fsentence = []
    for element in pinyin_strings:
        fsentence.append(' '.join(element))

    for sentence in fsentence:
        new_sent = format_fsentence(sentence)
        fsentence.append(new_sent)
        fsentence.remove(sentence)

    return '\n'.join(fsentence)

"""Shows names more clearly in the pinyin, and formats various parts of the
strings to look pretty"""
def format_fsentence(formatted_sent):
    # Be careful the dictionary values and keys are all unique, if a key
    # and value are the same somewhere, you could get unintended replaces
    removal_dict = {
            "msgstr   ": "", "m s g s t r  ": "", "。 ": "。", " 。": "。", "， ": "，",
            " ，": "，", " ： ": "：", " \\ n": "\\n", "\\ n": "\\n",
            " ！": "！",
            " \\ ": "\\", " \"": "\"", " !": "!", " ？": "？", "\" ": "\"",
            " - ": "-", "> ": ">", " , ": ",", " — — ": "——", " -- > ": "-->",
            "* * * ": "***", "“ ": "“", " ”": "”", "… …": "……",
            "\"¥ 9,000。\"\n": "",
            "$ ( l . n a m e )": "$(l.name)", "$ ( l . s i r )": "$(l.sir)",
            "$ ( s . n a m e )": "$(s.name)",
            "$ + ( l . h o n o r i f i c )": "$+(l.honorific)",
            "$ + ( l . n a me )": "$+(l.name)",
            "$ ( l . m a n )": "$(l.man)", "$ ( l . g u y )": "$(l.guy)",
            "$ ( s . m a n )": "$(s.man)", "$ ( s . g u y )": "$(s.guy)",
            "$ ( l . R a c e )": "$(l.Race)", "$ ( l . S i r )": "$(l.Sir)",
            "$ + ( l . g u y )": "$+(l.guy)", "$ ( l . N a m e )": "$(l.Name)",
            "$ ( l . r a c e )": "$(l.race)", "$ + ( l . s i r )": "$+(l.sir)",
            "$ ( l . r a c e _ p l u r a l )": "$(l.race_plural)",
            "$ + ( l . r a c e _ p l u r a l )": "$+(l.race_plural)",
            "$ ( l . h i m )": "$(l.him)", "$ ( l . h e )": "$(l.he)",
            "$ ( l . h e )": "$(l.he)",
            "$ ( l . h i s )": "$(l.his)", "$ + ( l . h e )": "$+(l.he)",
            "$ ( l . s e x )": "$(l.sex)", "$ ( s . N a m e )": "$(s.Name)",
            "$ ( s c e n e . B r o S i s )": "$(scene.BroSis)",
            "$ ( s c e n e . F a t h e r M o t h e r )  ": "$(scene.FatherMother)",
            "$ ( s c e n e . T a l k A b o u t ) ": "$(scene.TalkAbout)",
            "pa4 ke1": "Pa4ke1", "mai4 ku4 lu2 Si1 ji1": "Mai4ku4lu2si1ji1",
            "mei2 ku4": "Mei2ku4",
            "Ai1 li3 ke4": "Ai1li3ke4", "yin2 xing1": "Yin2xing1",
            "kai3 yue1 ti2": "Kai3yue1ti2",
            "jie2 xi1 ka3": "Jie2xi1ka3", "mo4 ni1 ka3": "Mo4ni1ka3",
            "ji2 nuo4": "Ji2nuo4", "wei1 er3 Si1": "Wei1er3si1",
            "Bo1 te4 lan2": "Bo1te4lan2",
            "lai2 ke4": "Lai2ke4", "xi1 la1 Si1": "Xi1la1si1",
            "fu2 Si1 ba4 ge2": "Fu2si1bo2ge2",
            "shan1 mu3": "Shan1mu3", "Hua2 zi1": "Hua2zi1", "sa4 mi3 di4": "Sa4mi3di4",
            "shan1 ge1 ma3": "Shan1ge1ma3",
            "ku4 Bo1 ta3": "Ku4bo1ta3", "gu3 ma3 er3": "Jia3ma3er3", "sa4 li4": "Sa4li4",
            "ba1 long1": "Ba1long2",
            "kong1 tong3 shi4": "Kong1tong3shi4",
            "xiong1di4hui4": "Xiong1di4hui4",
            "yu2 mei2 lin2 da2": "Yu3mei2 Lin2da2",
            "ku4 lu3": "Ku4lu3", "ha1 li4 Bo1 te4": "Ha1li4 Bo1te4",
            "te4 li3 Si1 tan3": "Te4li3si1tan3", "Ha1li4 kui2 yin1": "Ha1li4kui2yin1",
            "huo4 ling2 Si1": "Huo4ling2si1", "mo4 Si1 man4": "Mo4si1man4",
            "Ai1 ke4": "Ai1ke4", "la1 rui4": "La1rui4", "duo1 De2": "Duo1de2",
            "De2 lai2 Si1 deng1": "De2lai2si1deng1",
            "niu3 la1 rui4": "Niu3la1rui4",
            "A1 er3 jie2 nong2": "A1'er3jie2nong2", "A1 li4 ke4 Si1": "A1li4ke4si1",
            "（ ": "（", " ）": "）",
            " { { G M } } ": "{{GM}}", " { { / G M } } ": "{{/GM}}",
            "{ { / G M } }": "{{/GM}}", "{ { G M } }": "{{GM}}",
            " { { / G M } }": "{{/GM}}", "{ { C C } }": "{{CC}}",
            "{ { / C C } }": "{{/CC}}",
    }

    regex_patterns = ["\"SEA\d\d\d-\d\d\d\"", "\"c\d\d _ Test.*\""]

    for key in removal_dict:
        if key in formatted_sent:
            formatted_sent = formatted_sent.replace(key, removal_dict[key])
    
    for pattern in regex_patterns:
        if re.match(pattern, formatted_sent):
            formatted_sent = ""

            

    return formatted_sent

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

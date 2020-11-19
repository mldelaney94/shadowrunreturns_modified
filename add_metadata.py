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
            print(line)

    g.close()
                
def get_pinyin_from_characters(zh_dict, list_of_sents):
    """ assumes a list of a list of strings """
    pinyin = []
    for sentence in list_of_sents:
        for word in sentence:
            if word in zh_dict:
                pinyin.append(zh_dict[word]['pinyin'])
            else:
                pinyin.append(word)

    return pinyin

def format_pinyin_into_paragraphs(pinyin_strings):
    """ assumes one list of lists of strings """
    fsentence = []
    for element in pinyin_strings:
        fsentence.append(' '.join(element))

    for sentence in fsentence:
        new_sent = remove_unwanted_parts_from_fsentence(sentence)
        fsentence.append(new_sent)
        fsentence.remove(sentence)

    return '\n'.join(fsentence)

def remove_unwanted_parts_from_fsentence(formatted_sent):
    # Be careful the dictionary values and keys are all unique, if a key
    # and value are the same somewhere, you could get unintended replaces
    removal_dict = {
            "msgstr   ": "", "。 ": "。", " 。": "。", "， ": "，",
            " ，": "，", " ： ": "：", " \\ n": "\\n", "\\ n": "\\n",
            " \\ ": "\\", " \"": "\"", " !": "!", " ？": "？", "\" ": "\"",
            " - ": "-", "> ": ">", " , ": ",", " — — ": "——", " -- > ": "-->",
            "* * * ": "***", "“ ": "“", " ”": "”",
            "\"¥ 9,000。\"\n": "",
            "$ ( l . name )": "$(l.name)", "$ ( l . sir )": "$(l.sir)",
            "$ ( s . name )": "$(s.name)", "$ + ( l . honorific )":
            "$+(l.honorific)", "$ + ( l . name )": "$+(l.name)",
            "$ ( l . man )": "$(l.man)", "$ ( l . guy )": "$(l.guy)",
            "$ ( s . man )": "$(s.man)", "$ ( s . guy )": "$(s.guy)",
            "$ ( l . Race )": "$(l.Race)", "$ ( l . Sir )": "$(l.Sir)",
            "$ + ( l . guy )": "$+(l.guy)", "$ ( l . Name )": "$(l.Name)",
            "$ ( l . race )": "$(l.race)", "$ + ( l . sir )": "$+(l.sir)",
            "$ ( l . race _ plural )": "$(l.race_plural)",
            "$ + ( l . race _ plural )": "$+(l.race_plural)",
            "$ ( l . him )": "$(l.him)", "$ ( l . he )": "$(l.he)",
            "$ ( l . his )": "$(l.his)", "$ + ( l . he )": "$+(l.he)",
            "$ ( l . sex )": "$(l.sex)", "$ ( s . Name )": "$(s.Name)",
            "$ ( scene . BroSis )": "$(scene.BroSis)",
            "$ ( scene . FatherMother )": "$(scene.FatherMother)",
            "$ ( scene . TalkAbout )": "$(scene.TalkAbout)",
            "帕科": "Pa4ke1", "麦库卢斯基": "Mai4ku4lu2si1ji1",
            "名歌手": "ming2 ge1shou3", "梅库": "Mei2ku4",
            "埃里克": "Ai1li3ke4", "银星": "Yin2xing1", "凯约": "Kai3yue1",
            "杰 希卡": "Jie2xi1ka3", "莫妮卡": "Mo4ni1ka3",
            "吉诺": "Ji2nuo4", "威尔斯": "Wei1er3si1", "求求": "qiu2qiu2",
            "救救": "jiu4jiu4", "波特兰": "Bo1te4lan2",
            "很多": "hen3duo1", "开膛手": "kai1tang2shou3", "毋": "wu2",
            "狂奔": "kuang2ben1", "莱克": "Lai2ke4",
            "fu2 斯伯格": "Fu2si1bo2ge2", "沉醉": "chen2zui4",
            "山姆": "Shan1mu3", "华兹": "Hua2zi1", "萨米 di4": "Sa4mi3di4",
            "萨米 蒂": "Sa4mi3di4", "姗戈玛": "Shan1ge1ma3",
            "库波塔": "Ku4bo1ta3", "贾马尔": "Jia3ma3er3", "萨利": "Sa4li4",
            "灵体们": "Ling2ti3men", "巴隆": "Ba1long2",
            "空统 shi4 xiong1di4hui4": "Kong1tong3shi4xiong1di4hui4",
            "统世 xiong1di4hui4": "Tong3shi4xiong1di4hui4",
            " 崔斯坦 ": "cui1si1tan3", "予梅琳 da2": "Yu3mei2lin2da2",
            "精神病院": "jing1shen2bing4yuan4", "库鲁": "Ku4lu3",
            "特里斯坦": "Te4li3si1tan3", "Ha1li4 奎因": "Ha1li4 Kui2yin1",
            "霍灵斯": "Huo4ling2si1", "默斯 man4": "Mo4si1man4",
            "埃克": "Ai1ke4", "深表同情": "shen1biao3tong2qing2",
            "豆制": "dou4zhi4", "趴下": "pa1xia4", "多德": "Duo1de2",
            "通讯器": "tong1xun4qi4", "盲眼": "mangyan3", "巨魔": "ju4mo2",
            "神经中枢": "shen2jing1 zhong1shu1",
            "（ ": "（", " ）": "）",
            " { { GM } } ": "{{GM}}", " { { /GM } } ": "{{/GM}}",
            "{ { / GM } }": "{{/GM}}", "{ { GM } }": "{{GM}}",
            " { { / GM } }": "{{/GM}}", "{ { CC } }": "{{CC}}",
            "{ { / CC } }": "{{/CC}}",
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

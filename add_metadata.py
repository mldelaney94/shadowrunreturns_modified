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

    print(list(jieba.cut("你好", cut_all=False)))

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
            "埃克": "Ai1ke4", "拉瑞": "la1rui4", "多德": "Duo1de2",
            "德莱斯 deng1": "De2lai2si1deng1",
            "深表同情": "shen1biao3tong2qing2",
            "豆制": "dou4zhi4", "趴下": "pa1xia4", 
            "通讯器": "tong1xun4qi4", "盲眼": "mangyan3", "巨魔": "ju4mo2",
            "神经中枢": "shen2jing1 zhong1shu1", "纽拉瑞": "Niu3la1rui4",
            "从未见过": "cóngwèi jiànguò", "一个": "yi1 ge4",
            "一片": "yi1 pian4", "酸液": "suan1 ye4", "弄成": "nong4cheng2",
            "并不知道": "bing4bu4 zhi1dao4", "喝得": "he1de5",
            "太醉": "tai4 zui4", "从未有过": "cong2wei4you3guo4",
            "那次": "na4ci4", "买来": "mai3lai2",
            "废话少说": "fei4hua4 shao3shuo1", "一笑": "yi1 xiao4",
            "一整天": "yi1 zheng3tian1", "抖个": "dou3 ge4",
            "真的": "zhen1 de5",
            "联络网": "lian2luo4wang3", "扔出": "reng1 chu1",
            "一丝": "yi1 si1", "那家伙": "na4 jia1huo5",
            "烧成灰": "shao1cheng2hui1", "舔着": "tian3 zhe5",
            "举起手来": "ju3qi3 shou3lai2", "脸上": "lian3shang4",
            "并不需要": "bing4bu4 xu1yao4", "一杯": "yi1 bei1",
            "绝不会": "jue2bu4 hui4", "不论如何": "bu4lun4 ru2he2",
            "最佳人家": "zui4jia1 ren2jia5", "发讯器": "fa1 xun4 qi4",
            "同生": "tong2sheng1", "释罪": "shi4 zui4", "发话": "fa1hua4",
            "伤己": "shang1 ji3", "糜乱": "mu2 luan4",
            "付出代价": "fu4chu1 dai4jia4", "十万": "shi2wan4",
            "一大堆": "yi1 da4 dui1",  "一枚": "yi1 mei2",
            "扫清": "sao3qing1", "si3wang2 发讯": "si3wang2fa1xun4",
            "发讯": "fa1xun4", "手术刀": "shou3shu4dao1",
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

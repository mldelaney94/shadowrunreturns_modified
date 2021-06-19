def combine_languages(fl, sl):
    if fl == '' or sl == '':
        print('Please specify what PO files you would like to combine')
        exit

    first_language_file_chunks = chunk_file(get_file_path(fl))
    second_language_file_chunks = chunk_file(get_file_path(sl))

    final_po = stitch_chunks(first_language_file_chunks, second_language_file_chunks)

    with open('final.po', 'w+') as f:
        f.write(final_po)

def get_file_path(prefix):
    return 'materials/translations/' + prefix + '_deadmanswitch.po'

def chunk_file(file_path):
    chunks = {}
    chunk_counter = 0
    with open(file_path) as f:
        chunk = []
        while (line := f.readline()):
            if line == '\n': #blank line in PO files
                chunks[chunk_counter] = chunk
                chunk_counter += 1
                chunk = []
            else:
                chunk.append(line)
    
    return chunks

'''Takes in two dictionarys with 6679 keys and stitches them together.
bottom refers to order in which the pieces will appear. Top language first,
then bottom language.
'''
def stitch_chunks(top_chunks, bottom_chunks):
    chunk_counter = 0
    final_po = ''
    while(chunk_counter < 6679): #every file has 6679 chunks
        top = ''.join(top_chunks[chunk_counter])
        bottom = ''.join(bottom_chunks[chunk_counter]).split('msgstr')
        bottom [1] = bottom[1].replace(' \"\"\n', '') #leftover from msgstr ""
        top += '\"\\n\"\n'*2 #for in-game display
        top += bottom[1].strip(' ')
        top += '\n' #without this there will be no separation
        final_po += top

        chunk_counter += 1

    return final_po

if __name__ == '__main__':
    combine_languages('it', 'ru')

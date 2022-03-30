import pandas as pd
import glob
import json
from konlpy.tag import Komoran, Hannanum

def read_json(directory='C:/Users/oian/Documents/NIA/NIKL_SPOKEN(v1.0)/Corpus'):
    path = directory
    files = glob.glob(path + "/*.json")
    li = []
    error = []
    for file in files:
        # print(file)
        try:
            with open(file, 'r', encoding='utf-8-sig') as file2:
                x = json.load(file2, strict=False)
                li.append(get_str(x))
        except:
            error.append(file)
    return li # error

def get_str(json_file): # take only the transcript from a json file
    meta = json_file['metadata']
    #file_name = meta['title'] + ' ' + meta['year']
    #category = meta['category'].split()[-1]
    doc = json_file['document'][0]
    #title = doc['metadata']['title']
    """
    try:
        topic = doc['metadata']['topic']
    except:
        topic = ''
    """
    utters = doc['utterance']
    transcript = []
    for utter in utters:
        transcript.append(utter['form'])
    return transcript # file_name, category, title, topic,
    """
    cols = ['파일명', '구분', '제목', '주제', '대본']
    df = pd.DataFrame(li, columns=cols)
    df.to_json('parsed.json', force_ascii=False)
    """

## parsing
def parse(file_list):
    parser = Komoran()
    parsed = []
    for file in file_list:
        for phrase in file:
            parsed.append(parser.pos(phrase))
    return parsed

def get_NA(parsed):
    parsed_list = parsed
    NNP_list = []
    NF_list = []
    NA_list = []
    for element in parsed_list:
        for token in element:
            if token[1] == 'NA':
                NNP_list.append(token[0])
            """
            elif token[1] == 'NF':
                NF_list.append(token[0])
            elif token[1] == 'NPP':
                NA_list.append(token[0])
            """
    return NA_list #NNP_list, NF_list,
test = read_json()
#print(test)
parsed = parse(test)
NA_list = get_NA(parsed)
"""
NNP, NF, NA = map(set,[NNP_list, NF_list, NA_list])
df_NNP, df_NF, df_NA = map(pd.DataFrame, [NNP, NF, NA])
df_NF.to_csv('NF.csv', index='False', encoding='utf-8-sig')
df_NA.to_csv('NA.csv', index='False', encoding='utf-8-sig')
"""
df_NA = set(NA_list)
df_NA.to_csv('NA.csv', index='False', encoding='utf-8-sig')
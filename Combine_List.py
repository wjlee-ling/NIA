import pandas as pd
import re

def check(old_list, new_df):
    new_list = []
    print('=======================')
    for item in set(new_df['상황']):
        entity = re.match(r'[\w ]+', item).group().strip()
        entity = re.sub(' ', '', entity)
        for old_item in old_list:
            if re.search(entity, old_item) and len(re.search(entity, old_item).group()) >= 2:
                print(f'새 개체명 {entity} 이/가 예전 {old_item} 과 겹치지 않나요')
        new_list.append(entity)
    old_list = old_list.__add__(new_list)
    old_list.sort()
    print('누적 세트 갯수는 {} 입니다'.format(len(old_list)))
    return old_list

def to_excel(df, week):
    df.to_excel('외래어_개체명_축적_'+week)

# Set 1
existing_set = set()
xls = pd.ExcelFile(r'C:\Users\oian\Documents\NIA\외래어_개체명_Set1\외래어 스크립트(2)_한국외대.xlsx')
for sheet in xls.sheet_names:
    current_df = xls.parse(sheet)
    existing_set.update(current_df['개체명(한글)'])
first_list = sorted(existing_set) # returns a list
print(f'set 1의 총 단어 개수는: {len(first_list)}')

# Set 2
new_df = pd.read_excel('C:/Users/oian/Documents/NIA/외래어_개체명_Set2/외래어_스크립트_양식(최종)_jspark_개체명_Set2.xlsx', sheet_name= '개체명 외래어')
second_list = check(first_list, new_df)

# Set 3
new_df = pd.read_excel('C:/Users/oian/Documents/NIA/외래어_개체명_Set3/제공완료 [3차스크립트] 개체명 외래어 3차 스크립트_200929_2차검수취합2.xlsx', sheet_name= 0)
third_list = check(second_list, new_df)
df = pd.DataFrame(third_list)

# Set 4
new_df = pd.read_excel(r'C:\Users\oian\Documents\NIA\외래어_개체명_Set4\제공완료 [4차스크립트] 개체명 외래어 4차 스크립트_201008_2차검수취합_최종2.xlsx', header=0)
fourth_list = check(third_list, new_df)
df = pd.DataFrame(fourth_list)

# Set 5_partial
new_df = pd.read_excel(r'C:\Users\oian\Documents\NIA\외래어_개체명_Set5\외래어_스크립트_양식(최종)_jspark_개체명_Set5_작업중.xlsx')
fifth_list = check(fourth_list, new_df)
df= pd.DataFrame(fifth_list)
df.to_excel('개체명_외래어_5주차_누적.xlsx', header= None)

#execution
import named_entity_template_ver6 as ne
import pandas as pd
import re

df = pd.read_excel(r'C:\Users\oian\Documents\NIA\외래어_개체명_Set1\[1차스크립트] 외래어 스크립트(2)_한국외대_수정.xlsx', header=0)

for row in range(len(df['지문'])):
    if row % 3 == 0:
        entity = re.match(r'[\w ]+', df['상황'][row]).group().strip()
        ne.check_env(df['지문'][row], entity)
        ne.check_env(df['지문'][row+1], entity)
        ne.check_env(df['지문'][row+2], entity)
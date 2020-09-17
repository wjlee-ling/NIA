"""
'외래어_스크립트_양식(최종)'내 중분류 범주에 따라 주어진 외래어 개체명에 맞는 
"""
import pandas as pd
import random
import re
direc = ''
songs = pd.read_csv(direc, encoding='utf-8', header=0, nrows=100)

template_songs = ['제가 제일 좋아하는 노래는 {}이에요.', '{} 틀어줘.', '너 어제 나온 {} 들어봤어?', '{} 부른 가수가 누구지?']
template_movies = ['오늘 방송에서 {} 하더라.', '{}가 언제 개봉했지?', '전 {}가 그렇게 재미있는지 모르겠어요.', '영화 {} 정보 검색해줘'] # 2,3번 이/가
template_tvseries = ['제일 재미있게 보는 방송은 {}이에요.', '{} 방송시간 알아?', '어제 했던 {} 어땠어요?', '요즘 {} 보는 맛에 살아.'] #2
template_games = ['{}보다 재밌는 게임이 있을까?', '이따가 집에 가면 {} 한 판 하자.', '요즘 {} 안하는 사람 없어요.', '{}만 하면 몇 시간은 금방 가요.']
categories = {'SW':'SW', '음식': 'food', '제품':'product', '가수':'singer', '사업가':'businessperson', '영화인':'moviecrew', '정치인':'politician', 
              '기업체':'company','노래':'popsong', '영화':'movie', 'tv방송':'tvseries', '게임타이틀':'game'}

def write_scripts(df):
    for row in range(len(df['상황'])):
        entity = re.match('[\w 0-9]+', df['상황'][row]).group()
        cateogry = df['소분류'][row] # error when null??
        if category in categories:
            sentences = random.sample(template, k=3)
            df.at[row, '지문'] = sentences[0].format(entity)
            df.at[row, '지문'] = sentences[1].format(entity)
            df.at[row, '지문'] = sentences[2].format(entity)
    return df

def choose

def is_jong(character):
    cc = ord(character) - 44032  # 한글 완성자의 유니코드 포인터 값 추출
    cho = cc // (21 * 28)  # 초성 값 추출
    jung = (cc // 28) % 21  # 중성 값 추출
    jong = cc % 28  # 종성 값 추출
    result = 0 if jong == 0 else 1 #종성 없으면 0 있으면 1
    return result

def print_out(df):
    df.to_csv(encoding='utf-8-sig')
    
write_scripts(tvseries, template_tvseries, 'scripted_tvseries')



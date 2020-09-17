import pandas as pd
import random
import re
songs = pd.read_csv('C:\\Users\\oian\\Documents\\NIA\\named_entity_songs.csv', encoding='utf-8', header=None, nrows=27)
movies = pd.read_csv('C:\\Users\\oian\\Documents\\NIA\\named_entity_movies.csv', encoding='utf-8', header=None, nrows=43)
tvseries = pd.read_csv('C:\\Users\\oian\\Documents\\NIA\\named_entity_tvseries.csv', encoding='utf-8', header=None, nrows=22)
games = pd.read_csv('C:\\Users\\oian\\Documents\\NIA\\named_entity_gametitles.csv', encoding='utf-8', header=None, nrows=27)

template_songs = ['제가 제일 좋아하는 노래는 {}이에요.', '{} 틀어줘.', '너 어제 나온 {} 들어봤어?', '{} 부른 가수가 누구지?']
template_movies = ['오늘 방송에서 {} 하더라.', '{}가 언제 개봉했지?', '전 {}가 그렇게 재미있는지 모르겠어요.', '영화 {} 정보 검색해줘'] # 2,3번 이/가
template_tvseries = ['제일 재미있게 보는 방송은 {}이에요.', '{} 방송시간 알아?', '어제 했던 {} 어땠어요?', '요즘 {} 보는 맛에 살아.'] #2
template_games = ['{}보다 재밌는 게임이 있을까?', '이따가 집에 가면 {} 한 판 하자.', '요즘 {} 안하는 사람 없어요.', '{}만 하면 몇 시간은 금방 가요.']

def fill_in(df, template, save_name):
    for row in range(len(df[0])):
        entity = re.match('[\w 1-9]+', df[0][row]).group()
        sentences = random.sample(template, k=3)
        df.at[row, 2] = sentences[0].format(entity)
        df.at[row, 3] = sentences[1].format(entity)
        df.at[row, 4] = sentences[2].format(entity)
    return df.to_csv('C:\\Users\\oian\\Documents\\NIA\\'+save_name+'.csv', index=False, encoding='utf-8-sig')
def is_jong(character):
    cc = ord(character) - 44032  # 한글 완성자의 유니코드 포인터 값 추출
    cho = cc // (21 * 28)  # 초성 값 추출
    jung = (cc // 28) % 21  # 중성 값 추출
    jong = cc % 28  # 종성 값 추출
    result = 0 if jong == 0 else 1 #종성 없으면 0 있으면 1
    return result

#fill_in(songs, template_songs, 'scripted_songs')
#fill_in(movies, template_movies, 'scripted_movies')
fill_in(tvseries, template_tvseries, 'scripted_tvseries')
#fill_in(games, template_games, 'scripted_games')


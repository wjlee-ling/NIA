"""
ver_2는 원치않는 위치의 조사를 바꾸는 경우가 있었음. e.g. '그녀는 눈는 안좋다' 라는 문장을 '그녀은 눈는 안좋다'로 바꿈.
csv파일에서 entity 추출시 str앞뒤에 있을 수 있는 스페이스를 제거함
csv파일에서 theme 추출시 알파벳 대/소문자 관련 문제를 해결함
csv파일 대신 excel로 읽기

write_script 함수에 작성자 이름 기입해야함.


template_clothes (의류 포함)
"""

import pandas as pd
import random
import re
import numpy as np

categories = {'SW':'sw', '음식': 'food', '제품':'product', '가수':'singer', '사업가':'businessperson', '영화인':'moviecrew', '정치인':'politician',
              '기업체':'company','노래':'song', '영화':'movie', 'TV방송':'tvseries', '게임타이틀':'game', '체육인':'sportsperson', '의류':'clothes'}

template_song = ['크게 {} 틀어줘.', '어떤 가수가 {}를 불렀는지 알아?', '요즘엔 {} 즐겨 들어요.', '통화연결음 {}로 바꿨는데 어때?', '노래방에서 {}는 꼭 불러요.',
                 '운전할 때 {}도 즐겨 들어요.', '그 가수의 대표곡이 {}야?', '스피커로 {} 꼭 들어봐.']
template_movie = ['특선영화로 {}를 방영한대.', '내일 {}가 개봉해요.', '전 {} 별로 재미없었어요.', '영화 {} 정보 검색해줘.', '벌써 {} 예매했어?',
                  '그 배우가 {}에 출연했어?', '그 감독이 {}도 만들었어요?', '내 친구 {} 스태프였어.', '개봉하면 꼭 {} 챙겨 봐.']
template_tvseries = ['월요일엔 꼭 {} 챙겨 봐야 해.', '어제 {} 재밌었어요?', '지난 주에 {} 봤어요?','컴퓨터로 {} 다시 보자.', '요즘 {}만 챙겨 봐요.'
                     '그 연예인이 {}에도 나와요?', '시청률은 {}가 제일 높아요.', '공부하느라 {}를 못 봤네.', '빨리 {} 시작했으면 좋겠다.']
template_game = ['게임 중에 {}가 제일 재밌어.', '이따가 집에 가면 {} 한 판 하자.', '요즘 {} 안하는 사람 없어요.', '주말에 {}만 하면 몇 시간은 금방이야.',
                 '모바일로도 {}를 할 수가 있어?', '난 {}는 너무 시시해서 안 해.', '게임 좋아하면 {}는 쉽게 할거야.', '퇴근하고 빨리 {} 하고 싶어.']
template_company = ['가장 선호하는 직장은 {}예요.', '내 동생 {}에서 알바했어.', '어제 {} 채용공고 올라온 거 봤어?', '내 친구 {}에서 인턴한대.',
                    '어제 {} 주가가 폭락했어요.', '곧 {} 주가가 오를 것 같아요.', '복지는 {}가 가장 유명해.', '오늘부터 {}로 출근해요.', '가능하면 {}로 이직하고 싶어.',
                    '일 힘든 걸로는 {}가 제일 유명해.']
template_food = ['난 {}만 먹으면 속이 별로야.', '내일 오랜만에 {} 먹을래?', '은근히 {}를 싫어하는 사람 많아요.', '집에 올 때 {}를 사 와.',
                 '우리 {} 시켜 먹을까?', '주변에 {} 맛있는 집 알아?', '이 집은 {}로 가장 유명해요.', '여기 {} 하나 주세요.', '요즘 {}만 먹어요.',
                 '스트레스 받으면 {}가 당겨.', '엄마도 {}를 좋아할까?', '빨리 {} 시키자.']
template_product = ['요즘에 {}를 즐겨 써요.', '지금 쓰는 {}는 너무 오래됐어.', '요즘 {} 중고가는 얼마예요?', '생일선물로 {}를 받았어.', '가성비를 따져 보니 {}는 별로야.',
                    '제 주위엔 다 {} 써요.', '내 친구도 {}를 쓴대.', '해외에 가면 {} 꼭 사야지.', '돈이 없어 {}는 못 사.', '백화점에서 {}를 팔더라.',
                    '그 {} 어디서 샀어?', '할인하길래 {} 샀어.', '이제 {} 없이 못 살겠어.']
template_singer = ['어제 {} 공연 갔어?', '그제 나온 {} 신곡 좋더라.', '한번이라도 {} 들어 봤어?', '요즘 {} 앨범만 들어.', '미국에서도 {} 인기가 대단하대.',
                   '은근히 {}도 노래 잘해.', '이 곡 {} 노래야?', '노래 듣자마자 {} 팬이 됐어.', '가수 중 {}를 가장 좋아해요.', '뉴스 보니 {}가 기부했대요.',
                   '내일 {} 컴백한대요.']
template_politician = ['요즘 {} 기사가 많이 나오더라.', '아직도 {} 영향력이 대단한가봐.', '한국에서 {} 인지도가 어느 정도야?', '다음달에 {}가 방한한대.',
                       '다음 선거에도 {}가 나올까?', '이번에 대통령과 {}가 만난대요.', '뉴스 보면 다 {} 얘기 뿐이야.', '넌 {}가 어디 정당인지 알아?']
template_businessperson = ['너는 {}에 대해 어떻게 생각해?', '그 회사 대표가 {}야?', '기업인 중에 {}를 가장 존경해요.', '그 자기계발서 {}가 썼대.', '언젠가 {}처럼 성공할거야.',
                        '너 {}의 경영철학에 대해 들어봤어?', '과감한 투자하면 {}지.', '최근에 {}가 크게 기부했대.', '그 회사 창업자가 {}예요?', '신기하게도 {}는 경영학 전공이 아니래.']
template_moviecrew = ['넌 왜 {}를 좋아해?', '그 영화는 {}의 대표작이 아니야.', '그 영화 감독이 {}야?', '영화광들은 {}를 좋아해.', '시상식에 {} 나온 거 봤어?',
                      '홍보차 {}가 방한한대요.', '그 배우랑 {}가 사귄대요.', '나는 예전부터 {} 팬이야.', '내일 {} 최신작이 개봉해요.']
template_sportsperson = ['나도 {} 선수 좋아해.', '기사 보니까 {}가 부상을 입었대.', '아쉽게도 {}도 예전 같지 않아요.', '운동선수 중에 {}를 제일 좋아해요.',
                         '오랜만에 {} 경기 보니깐 좋더라.', '그 배우랑 {}가 사귀잖아.', '아직 {}가 가장 잘해?',
                         '하루만 {}로 살아보고 싶다.', '외국에 가면 {} 경기는 꼭 볼거야.', '그 신발은 {}가 홍보하는 거야.']
template_sw = ['휴대폰에 {} 좀 깔아.', '너 {} 써 봤어?', '어르신들은 {} 쓰는 게 어렵대.', '요즘 {} 안 쓰는 사람도 있어?', '우리 아버지도 {} 자주 쓰셔.', '빨리 {} 다운로드 받아.']
template_clothes = ['네가 신은 {} 어디 제품이야?', '이 {} 새로 산 거야?', '그 {}는 어디서 샀어?', '할인하길래 {} 샀어.', '검정색 {} 입어 볼 수 있을까요?', '동생이랑 {} 같이 입어요.']

def write_script(df, name):
    df = sort_by_name(df)
    df = repeat_rows(df)
    for row in range(len(df['상황'])):
        #df.at[row, 'Set Nr.'] = row//3 + 1
        if row % 3 ==0 :
            entity = re.match('[\w ]+', df['상황'][row]).group().strip() # no punctuations !
            theme = df['소분류'][row].upper().strip()
            df.at[row, '발화자'] = 'A-1'
            df.at[row+1, '발화자'] = 'A-2'
            df.at[row+2, '발화자'] = 'A-3'
            df.at[row, '작성자'] = name
            df.at[row+1, '작성자'] = name
            df.at[row+2, '작성자'] = name
            if theme in categories:
                template = globals()['template_'+categories[theme]]
                sentences = random.sample(template, k=3)
                df.at[row, '지문'] = kor_agr(sentences[0].format(entity))
                df.at[row+1, '지문'] = kor_agr(sentences[1].format(entity))
                df.at[row+2, '지문'] = kor_agr(sentences[2].format(entity))
    return df.to_csv('scripted.csv', encoding='utf-8-sig')

def is_jong(character):
    cc = ord(character) - 44032  # 한글 완성자의 유니코드 포인터 값 추출
    #cho = cc // (21 * 28)  # 초성 값 추출
    #jung = (cc // 28) % 21  # 중성 값 추출
    jong = cc % 28  # 종성 값 추출
    return jong

def kor_agr(sent): #가/이, 로(는)/으로(는), 를/을, 예요/이에요, 야/이야, 는/은, 나/이나
    variant = {'가':'이', '를':'을', '는':'은', '야':'이야', '지':'이지','예요':'이에요', '는요':'은요', '로':'으로', '로는':'으로는', '로요':'으로요','로는요':'으로는요'}
    sent_checked = ''
    sent_to_check = sent
    m = re.search(r'(?<=(\w))(가|를|는|야|예요|는요|로|로는|로요|로는요)\b', sent_to_check)
    while m:
        if is_jong(m.group(1)) == 0: # 앞음절에 종성이 없을 때
            sent_checked += sent_to_check[:m.end()]
        else: # 앞음절에 종성이 있을 때
            if '로' in m.group() and is_jong(m.group(1)) == 8: # e.g. '호텔'+'(으)로' = '호텔로'
                sent_checked += sent_to_check[:m.end()]
            elif '는' in m.group() and m.group(1) != '있': #있는 -> 있은 방지
                sent_checked += sent_to_check[:m.end()]
            else:
                sent_checked += sent_to_check[:m.start()] + variant[m.group()] # e.g. '호텝' + '(으)로' = '호텝으로'
        sent_to_check = sent_to_check[m.end():]
        m = re.search(r'(?<=(\w))(가|를|는|야|예요|는요|로|로는|로요|로는요)\b', sent_to_check)
    sent = sent_checked + sent_to_check
    return sent

def repeat_rows(df):
    new_df = pd.DataFrame(np.repeat(df.values, 3, axis=0))
    new_df.columns = df.columns
    return new_df

def sort_by_name(df):
    new_df = df.sort_values(by=['상황'])
    return new_df

#df = pd.read_excel('C:\\Users\\oian\\Downloads\\외래어_스크립트_양식(최종)_jspark.xlsx', sheet_name= 1,  header=0)
#write_script(df, '이원재')
print(kor_agr('맛있는 식당'))

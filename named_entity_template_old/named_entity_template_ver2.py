import pandas as pd
import random
import re
import numpy as np

categories = {'SW':'SW', '음식': 'food', '제품':'product', '가수':'singer', '사업가':'businessperson', '영화인':'moviecrew', '정치인':'politician',
              '기업체':'company','노래':'song', '영화':'movie', 'TV방송':'tvseries', '게임타이틀':'game', '체육인':'sportsperson'}

template_song = ['내가 제일 좋아하는 노래는 {}예요.', '너무 심심하니깐 {} 틀어줘.', '어제 공개된 {} 들어봤어?', '어떤 가수가 {}를 불렀는지 알아?',
                 '가게마다 {}를 틀더라고요.', '난 우울할 땐 {}를 크게 틀어 놔.', '통화연결음 {}로 바꿨는데 어때?', '노래방에 가면 {}는 꼭 불러요.',
                 '운전하면서 {}를 즐겨 들어요.', '그 가수의 대표곡은 {}야.', '스피커를 사면 꼭 {} 들어봐.']
template_movie = ['명절 특선영화로 {}를 방영한대.', '다음주에 {}가 재개봉하는데 보러 갈래?', '전 {}가 그렇게 재미있는지 모르겠어요.', '영화 {} 정보 검색해줘', '영화관에서 {}를 봤어?',
                  '그 배우가 {}에 출연했어?', '그 감독이 {}도 만들었어요?', '내 인생영화는 {}예요.']
template_tvseries = ['주말엔 {}를 제일 재밌게 봐요.', '오늘 하는 {} 방송시간 알아?', '어제 했던 {} 재밌었어요?', '지난 주에 {} 봤어요?','요즘엔 {} 보는 맛에 살아.',
                     '그 연예인이 {}에도 나와요?', '시청률은 {}가 제일 높대요.', '공부하느라 {}를 못 봤네.']
template_game = ['게임 중에는 {}가 제일 재밌어.', '이따가 집에 가면 {} 한 판 하자.', '요즘 {} 안하는 사람 없어요.', '주말에 {}만 하면 몇 시간은 금방이야.',
                 '모바일로도 {}를 할 수가 있어?', '난 {}는 너무 시시해서 안 해.', '게임 좋아하면 {}는 쉽게 할거야.', '퇴근하고 빨리 {} 하고 싶어.']
template_company = ['가장 선호하는 직장은 {}예요.', '세계에 {}만한 기업이 있어?', '어제 {} 채용공고 올라온 거 봤어?', '내 친구 {}에서 인턴한대.',
                    '어제 {} 주가가 폭락했어요.', '곧 {} 주가가 오를 것 같아요.', '복지는 {}가 가장 유명해.', '오늘부터 {}로 출근해요.', '가능하면 {}로 이직하고 싶어.',
                    '일 힘든 걸로는 {}가 제일 유명해.']
template_food = ['난 {}만 먹으면 속이 별로야.', '내일 오랜만에 {} 먹을래?', '음식 중엔 {}를 가장 좋아해.', '은근 {}를 싫어하는 사람 많아요.', '집에 올 때 {}를 사 와.',
                 '우리 {} 시켜 먹을까?', '주변에 {} 맛있는 집 알아?', '이 집은 {}로 가장 유명해요.', '여기 {} 하나 주세요.', '요즘에는 {}만 먹어요.',
                 '스트레스 받으면 {}가 땡겨.', '선생님이 {}를 즐겨 드실까?']
template_product = ['요즘엔 {}를 즐겨 써요.', '지금 쓰고있는 {}는 너무 오래됐어.', '중고로 사면 {}는 얼마예요?', '생일선물로 {}를 받았어.', '가성비만 보면 {}는 별로야.',
                    '내 주위엔 다 {} 써요.', '내 친구도 {}를 쓴대.', '해외에 가면 {}는 꼭 사야지.', '돈이 없어서 {}는 못 사.', '인터넷에서 {}를 팔더라.',
                    '가성비로 {}만한 게 없어요.']
template_singer = ['어제 {} 공연 갔어?', '그제 나온 {} 신곡 좋더라.', '한번이라도 {} 노래 들어봤어?', '요즘엔 {} 노래만 들어.', '미국에서 {} 인기가 대단하대.',
                   '은근 {}도 노래 잘해.', '십대 사이에선 {}가 대세야.', '노래방 가면 {} 노래는 꼭 불러.', '이 노래를 {}가 불렀어?', '노래 듣자마자 {} 팬이 됐어.',
                   '가수 중엔 {}를 가장 좋아해요.', '고음하면 {}가 최고야.', '뉴스마다 {} 얘기더라.']
template_politician = ['요즘 {} 기사가 많이 나오더라.', '아직도 {} 영향력이 대단한가봐.', '미국에서 {} 지지도가 어느 정도야?', '다음달에 {}가 방한한대.',
                       '다음 선거에도 {}가 나온대.', '이번에 대통령과 {}가 만난대요.', '뉴스 보면 다 {} 얘기 뿐이야.', '넌 {}가 어디 정당인지 알아?']
template_businessperson = ['너는 {}에 대해 어떻게 생각해?', '그 회사 대표가 {}야?', '기업인 중엔 {}를 가장 존경해요.', '이번에 {}가 자기계발서를 냈대.', '난 {}처럼 성공할거야.',
                        '넌 {}의 경영철학에 대해 알아?', '과감한 투자하면 {}야.', '최근에 {}가 크게 기부했대.', '그 회사 창업자가 {}예요?', '신기하게 {}는 경영학 전공이 아니래.']
template_moviecrew = ['넌 왜 {}를 좋아해?', '그 영화는 {}의 대표작이 아니야.', '그 영화 연출자가 {}야?', '한국 영화광들은 {}를 좋아해.', '시상식에 {} 나온 거 봤어?',
                      '홍보차 {}가 방한한대요.', '그 배우랑 {}가 사귄대요.', '나는 예전부터 {} 팬이야.', '내일 {} 최신작이 개봉해요.']
template_sportsperson = ['나도 {} 선수 좋아해.', '기사 보니까 {}가 부상을 입었대.', '아쉽게도 {}도 예전 같지 않아요.', '운동선수 중엔 {}가 제일 좋아.',
                         '우리나라엔 {} 같은 선수는 없나?', '오랜만에 {} 경기 보니깐 좋더라.', '그 배우랑 {}가 사귀잖아.', '아직도 {}가 가장 잘해?',
                         '하루만 {}로 살아보고 싶다.', '외국에 가면 {} 경기는 꼭 볼거야.', '그 신발은 {}가 홍보하는 거야.']
template_sw = ['휴대폰에 {} 좀 깔아.', '너는 {} 써 봤어?', '어르신들은 {}가 어렵대.', '요즘 {} 안 쓰는 사람도 있어?']

def write_script(df):
    df = sort_by_name(df)
    df = repeat_rows(df)
    for row in range(len(df['상황'])):
        df.at[row, 'Set Nr.'] = row//3 + 1
        if row % 3 ==0 :
            entity = re.match('[\w ]+', df['상황'][row]).group() # no punctuations !
            theme = df['소분류'][row]
            df.at[row, '발화자'] = 'A-1'
            df.at[row+1, '발화자'] = 'A-2'
            df.at[row+2, '발화자'] = 'A-3'
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

def kor_agr(sentence): #는/은, 가/이, 로/으로, 를/을
    if re.search('[를는가로] ', sentence) or re.search('\B(예요|야)', sentence):
        for m in re.finditer('\B가(?= )', sentence):
            if is_jong(sentence[m.start()-1]) != 0:
                sentence = re.sub('\B가(?= )', '이', sentence, count=1)
        for m in re.finditer('\B로(?=[ 는은])', sentence):
            if is_jong(sentence[m.start()-1]) != 0 and is_jong(sentence[m.start()-1]) != 8: #if there is a jongseong in the preceding syllable other than 'ㄹ'
                sentence = re.sub('\B로(?=[ 는은])', '으로', sentence, count=1)
        for m in re.finditer('\B를(?= )', sentence):
            if is_jong(sentence[m.start()-1]) != 0:
                sentence = re.sub('\B를(?= )', '을', sentence, count=1)
        for m in re.finditer('\B는(?= )', sentence):
            if is_jong(sentence[m.start()-1]) != 0:
                sentence = re.sub('\B는(?= )', '은', sentence, count=1)
        for m in re.finditer('\B예요', sentence):
            if is_jong(sentence[m.start()-1]) != 0:
                sentence = re.sub('\B예요', '이에요', sentence, count=1)
        for m in re.finditer('\B야(?=\W)', sentence):
            if is_jong(sentence[m.start()-1]) != 0:
                sentence = re.sub('\B야(?=\W)', '이야', sentence, count=1)
    return sentence

def repeat_rows(df):
    new_df = pd.DataFrame(np.repeat(df.values, 3, axis=0))
    new_df.columns = df.columns
    return new_df

def sort_by_name(df):
    new_df = df.sort_values(by=['상황'])
    return new_df

df = pd.read_csv('외래어_스크립트_양식(최종).csv', encoding='utf-8-sig', header=0)
write_script(df)
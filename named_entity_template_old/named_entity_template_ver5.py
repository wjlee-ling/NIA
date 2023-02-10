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

template_song = ['라디오에서 꼭 {} 틀어 주세요.', '누가 {}를 불렀는지 알아?', '요즘 {}만 들어.', '통화연결음을 {}로 바꿨는데 어때?', '노래방에서 {}는 꼭 불러요.',
                 '최근에 {}도 즐겨 들었어요.', '그 가수의 대표곡이 {}야?', '집에 가면 {} 꼭 들어봐.']
template_movie = ['특선 영화로 {}를 방영한대.', '내일 {}가 재개봉해요.', '난 {}는 생각보다 별로였어.', '영화 {} 정보 검색해 줘.', '어제 {} 시사회 다녀왔어.',
                  '그 배우가 {}에 나와?', '그 감독이 {}도 만들었어요?', '내 친구 {} 촬영 스태프였어.', '재개봉하면 꼭 {} 보러 가자.']
template_tvseries = ['주말엔 꼭 {} 챙겨 봐야 해.', '어제 {} 재밌었어요?', '컴퓨터로 {} 다시 보자.', '요즘 {}만 챙겨 봐요.',
                     '그 연예인이 {}에도 나왔어요?', '공부하느라 {}를 못 봤네.', '운동하면서 {} 한 편을 다 봤어.']
template_game = ['게임 중에 {}가 제일 재밌어.', '이따가 {} 한 판 하자.', '요즘 {} 안 하는 사람 없어요.', '너랑 {}만 하면 시간이 금방 가.',
                 '컴퓨터/모바일로도 {}를 할 수가 있어?', '난 {}도 재미 없더라고.',  '휴대폰/컴퓨터 사고 빨리 {} 깔아야지.']
template_company = ['가장 좋아하는 브랜드/카페/호텔/어쩌구는 {}예요.', '나랑 {}에서 알바/인턴 하자.', '내일 {} 할인해요.', '어제 {} 채용 공고 올라온 거 봤어?',
                    '곧 {} 주가가 오를 것 같아요.', '여기 {} 매장 있어요?', '이따가 {} 본사도 한번 가 보자.', '월요일부터 {}로 출근해요.']
template_food = ['오랜만에 {} 어때?', '마트에서 {} 좀 사 올래?', '저는 {} 하나 주세요.', '요즘 {}가 당겨.', '너는 꼭 {}를 시키더라.',
                 '나랑 {} 마실래?/먹을래?', '점심/후식으로 {}는 어때?', '여기 {} 안 좋아하는 사람 있어?', '이따가 {}도 시킬까?']
template_product = ['지금 쓰는 {}는 너무 오래됐어.', '요즘 {}가 필요해요.', '선물로 {}를 받았어.', '이번에 {} 하나 샀어요.',
                    '저 배우가 {} 모델이잖아.', '그거 사느니 {} 살래.', '!!직접작성! 제품 특성에 맞게']
template_singer = ['어제 {} 공연 봤어?', '그제 나온 {} 신곡 좋더라.', '한번이라도 {} 들어 봤어?', '요즘 {} 인기가 대단하대.',
                   '은근히 {}도 노래 잘해.', '이 곡 {} 노래야?', '노래 듣자마자 {} 팬이 됐어.', '가수 중에 {}를 가장 좋아해요.', '기사 보니 {}가 컴백한대요.']
template_politician = ['요즘 {} 기사가 많이 나오더라.', '아직도 {} 영향력이 대단한가봐.', '다음달에 {}가 방한한대.',
                       '이번에 대통령이 {}랑 만난대요.', '뉴스 보면 다 {} 얘기 뿐이야.', '난 {}에 대해서는 잘 몰라.']
template_businessperson = ['그 회사 대표가 {}야?', '기업인 중에 {}를 가장 존경해요.', '그 자기계발서를 {}가 썼대.', '꼭 {}처럼 성공할거야.',
                        '혹시 {}의 경영 철학에 대해 들어봤어?', '과감한 투자하면 {}지.']
template_moviecrew = ['그 영화는 {}의 대표작이 아니야.', '그 영화 감독이 {}야?', '그 화장품 {}가 홍보하는 거야.', '왜 {}는 예술 영화만 할까?',
                      '홍보차 {}도 방한한대요.', '그 가수랑 {}랑 사귄대요.', '나는 예전부터 {} 팬이야.', '내일 {} 최신작이 개봉해요.']
template_sportsperson = ['나도 {} 선수 좋아해요.', '기사 보니까 {}가 부상을 입었대.', '운동선수 중에 {}를 제일 좋아해요.', '그 배우랑 {}랑 사귀잖아.',
                         '열심히 훈련해서 {}처럼 되고 싶어.', '요즘 {}도 예전 같지 않더라고요.', '내 롤모델은 {}야.']
template_sw = ['휴대폰에 {} 좀 깔아.', '어르신들은 {}가 어렵대.', '요즘 {} 안 쓰는 사람도 있어?', '우리 부모님도 {}는 자주 쓰셔.',
               '빨리 {} 앱을 다운로드 받아.', '그 회사가 {}를 계발했대.', '휴대폰 사니까 {} 깔려 있던데?', '너 {} 써 봤어?']
template_clothes = ['네가 신은 {} 어디 제품이야?', '이 {} 새로 산 거야?', '그 {}는 어디서 샀어?', '요즘 {} 안 입는/신는 사람이 없어.', '나도 {} 한번 입어 볼래.']

def write_script(df, name):
    df = sort_by_name(df)
    df = repeat_rows(df)
    df['소분류'] = df['소분류'].astype(str)
    for row in range(len(df['상황'])):
        #df.at[row, 'Set Nr.'] = row//3 + 1
        if row % 3 ==0 :
            entity = re.match('[\w ]+', df['상황'][row]).group().strip() # no punctuations !
            theme = df['소분류'][row].upper().strip()
            df.at[row, '발화자'] = 'A-1'
            df.at[row+1, '발화자'] = 'A-2'
            df.at[row+2, '발화자'] = 'A-3'
            df.at[row:row+2, '작성자'] = name
            df.at[row:row+2, '상황'] = df.at[row, '상황'] + f"({df.at[row, 'Set Nr.']})"
            if theme in categories:
                template = globals()['template_'+categories[theme]]
                sentences = random.sample(template, k=3)
                df.at[row, '지문'] = kor_agr(sentences[0].format(entity))
                df.at[row+1, '지문'] = kor_agr(sentences[1].format(entity))
                df.at[row+2, '지문'] = kor_agr(sentences[2].format(entity))
    return df.to_excel(f'외래어_스크립트_양식(최종)_jspark_개체명_Set5_{name}.xlsx')

def kor_chr(character):
    cc = ord(character) - 44032  # 한글 완성자의 유니코드 포인터 값 추출
    cho = cc // (21 * 28)  # 초성 값 추출
    jung = (cc // 28) % 21  # 중성 값 추출
    jong = cc % 28  # 종성 값 추출
    return [cho, jung, jong]

def kor_agr(sent): #가/이, 로(는)/으로(는), 를/을, 예요/이에요, 야/이야, 는/은, 나/이나, 랑/이랑
    variant = {'가':'이', '를':'을', '는':'은', '야':'이야', '지':'이지','랑':'이랑','예요':'이에요', '는요':'은요', '로':'으로', '로는':'으로는', '로요':'으로요','로는요':'으로는요'}
    sent_checked = ''
    sent_to_check = sent
    m = re.search(r'(?<=(\w))(가|를|는|야|예요|는요|로|로는|로요|로는요)\b', sent_to_check)
    while m:
        if kor_chr(m.group(1))[2] == 0: # 앞음절에 종성이 없을 때
            sent_checked += sent_to_check[:m.end()]
        else: # 앞음절에 종성이 있을 때
            if '로' in m.group() and kor_chr(m.group(1))[2] == 8: # e.g. '호텔'+'(으)로' = '호텔로'
                sent_checked += sent_to_check[:m.end()]
            elif '는' in m.group() and m.group(1) == '있': #있는 -> 있은 방지
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

def check_env(df):
    for row in range(len(df['지문'])):
        if row % 3 == 0 :
            entity = re.match('r[\w ]+', df['상황'][row]).group().strip()

            if re.search('r[0-9]', entity):
                print(entity+'에는 숫자가 포함되어 있음. 지문에는 문자열로 썼는지 확인 바람.')
            else:
                sentences = [sent for sent in df['지문'][row:row+3]]
                prev, fol = [], []
                for sent in sentences:
                    prev_chr = kor_chr(re.search('\w\s?(?='+entity+')', sent).group().strip())
                    fol_chr = kor_chr(re.search('(?<='+entity+')\s?\w', sent).group().strip())
                    if prev_chr[2] == 0: # 앞 음절에 종성이 없으면
                        if prev_chr[1] in [1, 5]: # 앞 음절의 종성이 'ㅐ' 이거나 'ㅔ'이면
                            prev.append(1) # 'ㅐ' 추가
                        else:
                            prev.append(prev_chr[1]) # 앞 음절의 중성 추가
                    elif prev_chr[2] in [1, 2, 3, 9, 24]: # 종성이 'ㄱ', 'ㄲ', 'ㄳ', 'ㄺ', 'ㅋ'
                        prev.append(1)
                    elif prev_chr[2] in [7, 19, 20, 22, 23, 25]: # 종성이 'ㄷ', 'ㅅ', 'ㅆ', 'ㅊ', 'ㅌ'
                        prev.append(7)
                    elif prev_chr[2] in [17, 18, 14, 26]: # 'ㅂ', 'ㅄ', ㄿ', 'ㅍ':
                        prev.append(17)
                    elif prev_chr[2] in [4, 5, 6]: #'ㄴ', 'ㄵ', 'ㄶ'
                        prev.append(4)
                    elif prev_chr[2] in [8, 11, 12, 13, 15]: #ㄹ, ㄼ, ㄽ, ㄾ, ㅀ
                        prev.append(8)
                    elif prev_chr[2] in [16, 10]: #ㅁ, ㄻ
                        prev.append(16)
                    if fol_chr[0] == 11: # 다음 음절 초성이 'ㅇ'이면
                        if fol_chr[1] in [1, 5]: # ㅐ/ㅔ
                            fol.append(fol_chr[1]) # ㅐ 추가
                        else:
                            fol.append(fol_chr[1])
                    else:
                        fol.append(fol_chr[0])
            if len(prev) != len(set(prev)):
                print(entity,'앞 음절에 중복 있음!')
            if len(fol) != len(set(fol)):
                print(entity, '뒤 음절에 중복 있음!')

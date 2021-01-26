# 데이터 로딩
def read_data(filename, encoding='cp949'):                # 읽기 함수 정의
  with open(filename, 'r', encoding=encoding) as f:
    data = [line.split('\t') for line in f.read().splitlines()]
    data = data[1:]                 # txt 파일의 헤더(id document label)는 제외하기
  return data

def write_data(data, filename, encoding='cp949'):         # 쓰기 함수도 정의
  with open(filename, 'w', encoding=encoding) as f:
    f.write(data)

data = read_data('C:/Users/zidis/PycharmProjects/bm_test/ratings.txt', encoding='cp949')         # 전체파일은 ratings.txt

print(len(data))
print(data[0])

# 전체 데이터 형태소 분석
import rhinoMorph

rn = rhinoMorph.startRhino()

morphed_data = ''
for data_each in data:
  morphed_data_each = rhinoMorph.onlyMorph_list(rn, data_each[1],
                                                pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'])
  joined_data_each = ' '.join(morphed_data_each)  # 문자열을 하나로 연결
  if joined_data_each:  # 내용이 있는 경우만 저장하게 함
    morphed_data += data_each[0] + "\t" + joined_data_each + "\t" + data_each[2] + "\n"

# 형태소 분석된 파일 저장
write_data(morphed_data, 'C:/Users/zidis/PycharmProjects/bm_test/ratings_morphed.txt', encoding='cp949')

# 형태소 분석된 데이터 로딩
data = read_data('ratings_morphed.txt', encoding='cp949')

print(len(data))
print(len(data[0]))
print(data[0])

# 감정사전 읽기
data_id = [line[0] for line in data]  # 데이터 id
data_text = [line[1] for line in data]  # 데이터 본문
data_senti = [line[2] for line in data]  # 데이터 긍부정 부분

positive = read_data('C:/Users/zidis/PycharmProjects/bm_test/positive.txt')  # 긍정 감정사전 읽기
negative = read_data('C:/Users/zidis/PycharmProjects/bm_test/negative.txt')  # 부정 감정사전 읽기

print("positive:", positive)
print("negatvie:", negative)

pos_found = []  # 각 문장에서 발견될 긍정어의 개수
neg_found = []  # 각 문장에서 발견될 부정어의 개수


def cntWordInLine(data, senti):
  senti_found = []
  for onedata in data:
    oneline_word = onedata.split(' ')  # 한 줄의 데이터를 공백 단위로 분리하여 리스트로 저장
    senti_temp = 0
    for sentiword in senti:
      if sentiword[0] in oneline_word:  # posword[0] 하여 리스트를 문자열로 추출
        senti_temp += 1  # 현재의 감정단어와 일치하면 숫자를 하나 올려 줌 (중복은 계산 안 함)
    senti_found.append(senti_temp)  # 현재의 줄에서 찾은 감성단어의 숫자를 해당 위치에 저장
  return senti_found


data_senti_poscnt = cntWordInLine(data_text, positive)  # 발견된 긍정 단어의 숫자 파악
data_senti_negcnt = cntWordInLine(data_text, negative)  # 발견된 부정 단어의 숫자 파악

print(data_senti_poscnt)
print(data_senti_negcnt)

# 감정점수 계산
# Pandas 데이터프레임으로 저장
import pandas as pd
newdata = pd.DataFrame({'id':data_id, 'text':data_text, 'original':data_senti,
                        'pos':data_senti_poscnt, 'neg':data_senti_negcnt})
senti_score = newdata['pos'] - newdata['neg']      # 긍정개수에서 부정개수를 뺌
newdata['senti_score'] = senti_score               # 그 수를 senti_score 컬럼에 저장

newdata.loc[newdata.senti_score > 0, 'new'] = 1    # 새로운 긍부정 기호
newdata.loc[newdata.senti_score <= 0, 'new'] = 0   # 새로운 긍부정 기호

# 처음에 기록된 긍부정과 새로 계산된 긍부정이 같은지 여부를 matched 컬럼에 저장
# original 컬럼은 문자로 되어 있으므로 숫자로 변환 뒤 비교
newdata.loc[pd.to_numeric(newdata.original) == newdata.new, 'matched'] = 'True'
newdata.loc[pd.to_numeric(newdata.original) != newdata.new, 'matched'] = 'False'

newdata.head()

# 원점수와 비교 및 저장
score = newdata.matched.str.count('True').sum() / (newdata.matched.str.count('True').sum() + newdata.matched.str.count('False').sum()) * 100
print(score)

newdata.to_csv('C:/Users/zidis/PycharmProjects/bm_test/newfile.csv', sep=',', encoding='cp949', index=False) 	# csv 저장
newdata.to_csv('C:/Users/zidis/PycharmProjects/bm_test/newfile2.txt', sep='\t', encoding='cp949', index=False) 	# 또는 txt 저장

# 시그모이드 점수 계산
import math
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

newdata['sigmoid'] = newdata.senti_score.apply(sigmoid)

# 형태분석된 데이터 로딩
def read_data(filename, encoding='cp949'):               # 읽기 함수 정의
  with open(filename, 'r', encoding=encoding) as f:
    data = [line.split('\t') for line in f.read().splitlines()]
    data = data[1:]                                      # txt 파일의 헤더(id document label)는 제외하기
  return data

def write_data(data, filename, encoding='cp949'):        # 쓰기 함수 정의
  with open(filename, 'w', encoding=encoding) as f:
    f.write(data)

data = read_data('C:/Users/zidis/PycharmProjects/bm_test/ratings_morphed.txt', encoding='cp949')

print(len(data))
print(len(data[0]))
print(data[0])

# 훈련데이터와 테스트데이터 분리 (자동)
data_text = [line[1] for line in data]      		# 데이터 본문
data_senti = [line[2] for line in data]     		# 데이터 긍부정 부분

from sklearn.model_selection import train_test_split
train_data_text, test_data_text, train_data_senti, test_data_senti = train_test_split(data_text, data_senti, stratify=data_senti)

# Counter 클래스를 이용해 각 분류가 훈련데이터와 테스트데이터에 같은 비율로 들어갔는지 확인해 본다
from collections import Counter
train_data_senti_freq = Counter(train_data_senti)
print('train_data_senti_freq:', train_data_senti_freq)

test_data_senti_freq = Counter(test_data_senti)
print('test_data_senti_freq:', test_data_senti_freq)

# 훈련데이터와 테스트데이터 분리 (수동)
import random
random.shuffle(data)                            		# 랜덤하게 섞는다

data_70 = int(len(data)*0.7)					              # 전체 데이터 크기의 70% 숫자를 찾는다
train_data = data[:data_70] 					              # 앞에서 70% 부분을 잘라 훈련데이터로
test_data = data[data_70:] 					                # 그 뒷부분을 테스트데이터로

print('train data length:', len(train_data))    		# 138212
print('test data length:', len(test_data))      		# 59235

# 훈련데이터 요소 분리
train_data_text = [line[1] for line in train_data]      	# 훈련데이터 본문
train_data_senti = [line[2] for line in train_data]     	# 훈련데이터 긍부정 부분

# 테스트데이터 요소 분리
test_data_text = [line[1] for line in test_data]        	# 테스트데이터 본문
test_data_senti = [line[2] for line in test_data]       	# 테스트데이터 긍부정 부분

# 행렬 형태로 변환
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(min_df=1).fit(train_data_text)

import joblib
joblib.dump(vect, 'visualMind_vect.pkl')

X_train = vect.transform(train_data_text)		           # 행렬 생성
print("X_train:\n", repr(X_train))			               # 생성된 행렬 개요

# 행렬 내용 관찰
feature_names = vect.get_feature_names()

# 머신러닝 알고리즘 적용
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
y_train = pd.Series(train_data_senti)
lr = LogisticRegression(solver="liblinear")
lr.fit(X_train, y_train)

joblib.dump(lr, 'visualMind.pkl')
lr2 = joblib.load('4.pkl')

# 테스트 데이터 입력
X_test = vect.transform(test_data_text)
y_test = pd.Series(test_data_senti)
print("테스트 데이터 점수:", lr.score(X_test, y_test))

# 형태소분석기 시작
import rhinoMorph
rn = rhinoMorph.startRhino()

# 형태소 분석
new_input = '안녕하세요 어린이보험 중에 좋은 상품 문의 드립니다.'
inputdata = []
morphed_input = rhinoMorph.onlyMorph_list(rn, new_input, pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'])
morphed_input = ' '.join(morphed_input) # ['오늘', '정말', '재미있', '하루＇]를 한 개 문자열로 변환

inputdata.append(morphed_input)         # 분석 결과를 리스트로 만들기
print('input data:', inputdata)         # ['오늘 정말 재미있 하루']

X_input = vect.transform(inputdata)	    # 앞에서 만든 11445 컬럼의 행렬에 적용
result = lr2.predict(X_input) 	          # 0은 부정,1은 긍정

print(result)

if result == "0":
  print("부정적인 글입니다")
else:
  print("긍정적인 글입니다")
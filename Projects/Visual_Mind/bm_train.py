
import rhinoMorph
import collections as col
import matplotlib as mpl
import matplotlib.pyplot as plt
import json, requests
from flask import Flask, render_template, Response

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

def bokeh_with_json():
    return render_template('bokeh_with_json.html')

def plot_template(plot):
    from bokeh.plotting import figure
    from bokeh.embed import components
    from flask import Markup

    script, div = components(plot)
    script = Markup(script)
    div = Markup(div)
    return render_template('plot_template.html', plot1_script=script, plot1_div=div)

def bokeh_json_item2(sorted_keys_sample, sorted_values_sample):
    from bokeh.plotting import figure, show, output_file  # output_file = output as HTML
    from bokeh.models.tools import HoverTool  # for hover tooltip
    from bokeh.models import Axis, ColumnDataSource  # for axis settings
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Spectral6
    from bokeh.plotting import figure
    from bokeh.embed import json_item

    new_dict = dict()
    new_dict2 = dict()
    i = 0

    for item in sorted_keys_sample:
        if item != '':
            new_dict2[item] = sorted_values_sample[i]
            i += 1

    # 재정렬
    new_dict = dict(sorted(new_dict2.items(), key=lambda item: item[1]))

    print(new_dict.keys(), new_dict.values())

    viewCount = 10

    key_list = list(new_dict.keys())
    value_list = list(new_dict.values())

    fruits = key_list[len(key_list) - viewCount:]
    counts = value_list[len(value_list) - viewCount:]

    source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))

    output_file("colormapped_bars.html")
    p = figure(plot_width=500, plot_height=600,
               y_range=fruits,  # use the list as the range of y values
               toolbar_location=None,
               min_border=0)  # remove the toolbar since it isn't needed for this plot

    # p.hbar(y='fruits', right='counts', source=source, height=0.7, line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))
    p.hbar(y='fruits', right='counts', source=source, height=0.8, line_color='white',
           fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits[len(fruits) - 6:]))

    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.x_range.start = 0  # start value of the x-axis
    hover = HoverTool()  # initiate hover tool
    hover.tooltips = [("단어명", "@fruits"),  ## define the content of the hover tooltip
                      ("단어수", "@counts")]
    hover.mode = 'hline'  # set the mode of the hover tool
    p.add_tools(hover)  # add the hover tooltip to the plot
    # style the plot
    p.xaxis.major_label_text_font = 'IBM Plex Mono'
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font = 'IBM Plex Mono'
    p.yaxis.major_label_text_font_size = '13pt'
    # output the HTML file
    #output_file("neighborhoods.html", title='Neighborhoods with the most Black police killings')
    #show(p)  # show in notebook

    # json.loads 는 json으로 된 string을 dictionary로 변경해주는 것이고
    # json.dumps 는 dictionary를 json형식의 string으로 변경해주는 것이죠.
    return p

def bokeh_json_item(sorted_keys_sample, sorted_values_sample):
    from bokeh.plotting import figure, show, output_file  # output_file = output as HTML
    from bokeh.models.tools import HoverTool  # for hover tooltip
    from bokeh.models import Axis, ColumnDataSource  # for axis settings
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Spectral6
    from bokeh.plotting import figure
    from bokeh.embed import json_item

    new_dict = dict()
    new_dict2 = dict()
    i = 0

    for item in sorted_keys_sample:
        if item != '':
            new_dict2[item] = sorted_values_sample[i]
            i += 1

    # 재정렬
    new_dict = dict(sorted(new_dict2.items(), key=lambda item: item[1]))

    print(new_dict.keys(), new_dict.values())

    viewCount = 10

    key_list = list(new_dict.keys())
    value_list = list(new_dict.values())

    fruits = key_list[len(key_list) - viewCount:]
    counts = value_list[len(value_list) - viewCount:]

    source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))

    output_file("colormapped_bars.html")
    p = figure(plot_width=500, plot_height=600,
               y_range=fruits,  # use the list as the range of y values
               toolbar_location=None,
               min_border=0)  # remove the toolbar since it isn't needed for this plot

    # p.hbar(y='fruits', right='counts', source=source, height=0.7, line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))
    p.hbar(y='fruits', right='counts', source=source, height=0.8, line_color='white',
           fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits[len(fruits) - 6:]))

    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.x_range.start = 0  # start value of the x-axis
    hover = HoverTool()  # initiate hover tool
    hover.tooltips = [("단어명", "@fruits"),  ## define the content of the hover tooltip
                      ("단어수", "@counts")]
    hover.mode = 'hline'  # set the mode of the hover tool
    p.add_tools(hover)  # add the hover tooltip to the plot
    # style the plot
    p.xaxis.major_label_text_font = 'IBM Plex Mono'
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font = 'IBM Plex Mono'
    p.yaxis.major_label_text_font_size = '13pt'
    # output the HTML file
    output_file("neighborhoods.html", title='Neighborhoods with the most Black police killings')
    show(p)  # show in notebook

    ## 해당 개체를 json형식의 dictionary로 변경해줍니다.
    jsonified_p = json_item(model=p, target="myplot")
    # json.loads 는 json으로 된 string을 dictionary로 변경해주는 것이고
    # json.dumps 는 dictionary를 json형식의 string으로 변경해주는 것이죠.
    return json.dumps(jsonified_p, ensure_ascii=False, indent='\t')


def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper()  # 메소드이름을 대문자로 바꾼다
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':  # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST':  # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            print('22222')
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

    print('3333')
    """
    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}

    print('4444')
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}
    """

# 데이터 로딩
def read_data(filename, encoding='utf8'):                # 읽기 함수 정의
  with open(filename, 'r', encoding=encoding) as f:
    data = f.read()
    data = data[:]                 # txt 파일의 헤더(id document label)는 제외하기
  return data

def write_data(data, filename, encoding='utf8'):         # 쓰기 함수도 정의
  with open(filename, 'w', encoding=encoding) as f:
    f.write(data)

#data = read_data('/content/gdrive/My Drive/pytest/ratings_small.txt', encoding='cp949')
data = read_data('C:/Users/zidis/PycharmProjects/bm_test/RX.txt', encoding='utf8')  # 전체파일은 ratings.txt

rn = rhinoMorph.startRhino()
# 형태소 분석된 문장 샘플 보기
sample_data = rhinoMorph.onlyMorph_list(rn, data, pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'], eomi=True)

print('sample data:', sample_data)				            # 형태소 분석 결과
print('joined sample data:', ' '.join(sample_data))	  # 문자열을 공백으로 연결한다

morphed_data = ''
for data_each in sample_data:
  morphed_data_each = rhinoMorph.onlyMorph_list(rn, data_each,
                                                pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'],
                                                eomi=True)
  joined_data_each = ' '.join([str(elem) for elem in morphed_data_each])
  if joined_data_each:  # 내용이 있는 경우만 저장하게 함
    morphed_data += data_each + "\n"

# 형태소 분석된 파일 저장
write_data(morphed_data, '3_morphed.txt', encoding='cp949')
#print(morphed_data)

data_text = morphed_data      	# 데이터 본문

mergedTextList = data_text.split('\n')   	# 결합된 요소들을 공백 단위로 분리하여 하나의 리스트로 만든다
print('mergedTextList:', mergedTextList)

wordInfo_sample = col.Counter(mergedTextList)
sorted_keys_sample = sorted(wordInfo_sample, key=wordInfo_sample.get, reverse=True)
print('BM 단어빈도 총합:', len(sorted_keys_sample))
print('BM 고빈도 단어:', sorted_keys_sample)

"""
for item in wordInfo_sample:
  wordInfo_sample[item] = float('{:.2f}'.format(wordInfo_sample[item] / sum(wordInfo_sample.values()) * 100))
  #print( '{:.2f}'.format(wordInfo_sample[item]))
"""

sorted_values_sample = sorted(wordInfo_sample.values(), reverse=True)

print('BM 고빈도 단어비율:', sorted_values_sample)

s = sum(wordInfo_sample.values())
for k, v in wordInfo_sample.items():
       pct = v / s * 100
      #print(k, pct)

def read_data2(filename, encoding='utf8'):  # 읽기 함수 정의
    with open(filename, 'r', encoding=encoding) as f:
        data = [line.split('\n') for line in f.read().splitlines()]
        data = data[:]  # txt 파일의 헤더(id document label)는 제외하기
    return data


data = read_data2('C:/Users/zidis/PycharmProjects/bm_test/3_morphed.txt', encoding='cp949')

#data_id = [line[0] for line in data]       		# 데이터 id
#data_text = [line[1] for line in data]     		# 데이터 본문
#data_senti = [line[2] for line in data]    		# 데이터 긍부정 부분

#data_text = [line[1] for line in data]     		# 데이터 본문

#plt.title('=== BM 단어비율 ===')

if(len(sorted_keys_sample) > 6):
    plt.bar(range(7), sorted_values_sample[:7])	  # X축의 위치, 각 x의 높이
    plt.xticks(range(7), sorted_keys_sample[:7])  	# X축의 위치, 각 x의 라벨
else:
    plt.bar(range(len(sorted_keys_sample)), sorted_values_sample[:])	  # X축의 위치, 각 x의 높이
    plt.xticks(range(len(sorted_keys_sample)), sorted_keys_sample[:])  	# X축의 위치, 각 x의 라벨
#plt.show()

    #newdict[sorted_keys_sample[item]] = sorted_values_sample[item]

#top_neighborhoods = killings_data[killings_data.race == 'black'].neighborhood.value_counts().head(7).to_frame().sort_values(by='neighborhood', ascending=True)

from bokeh.palettes import GnBu3, OrRd3


#sorted_keys_sample1 = sorted(sorted_keys_sample, key=sorted_keys_sample.get, reverse=True)
#sorted_values_sample1 = sorted(sorted_values_sample, key=sorted_values_sample.get, reverse=True)

#bokeh_json_item(sorted_keys_sample, sorted_values_sample)
#plot_template(bokeh_json_item2(sorted_keys_sample, sorted_values_sample))

url='http://192.168.1.165:7791'
#web_request(method_name='POST', url=url, dict_data=bokeh_json_item(sorted_keys_sample, sorted_values_sample).encode('utf-8'))

import plotly.express as px
import pandas as pd

embed_df = pd.DataFrame({'words':sorted_keys_sample[:10], 'count':sorted_values_sample[:10]})
print(embed_df)

fig = px.scatter(embed_df, x='words', y='count', hover_name='words', text='words', size='count', size_max=100
                 , template='plotly_white', labels={'words': 'Avg. Length<BR>(words)'}
                 , color_continuous_scale=px.colors.sequential.Sunsetdark)

fig.update_traces(marker=dict(line=dict(width=1, color='Gray')))
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.show()
#web_request(method_name='POST', url=url, dict_data=fig.to_json().encode('utf-8'))


rn2 = rhinoMorph.startRhino()

# 형태소 분석
#new_input = '오늘은 정말 재미있는 하루구나!'
inputdata = []
#morphed_input = rhinoMorph.onlyMorph_list(rn2, data, pos=['NNG', 'NNP', 'VV', 'VA', 'XR', 'IC', 'MM', 'MAG', 'MAJ'])
#morphed_input = ' '.join(data) # ['오늘', '정말', '재미있', '하루＇]를 한 개 문자열로 변환

#print('input data:', morphed_data)         # ['오늘 정말 재미있 하루']
morphed_data = ''

for data_each in data:
    joined_data_each = ' '.join(morphed_data_each) # 문자열을 하나로 연결

    if joined_data_each: # 내용이 있는 경우만 저장하게 함
        morphed_data += data_each[0] + ' '

#inputdata.append(morphed_data)         # 분석 결과를 리스트로 만들기
mergedTextList = morphed_data.split(' ')
morphed_input = ' '.join(mergedTextList)
inputdata.append(morphed_input)

print('input data:', inputdata)         # ['오늘 정말 재미있 하루']

from sklearn.feature_extraction.text import CountVectorizer
import joblib

vect = joblib.load('4_vect.pkl')

X_input = vect.transform(inputdata)	              # 앞에서 만든 11445 컬럼의 행렬에 적용

lr2 = joblib.load('4.pkl')
result = lr2.predict(X_input) 	                  # 0은 부정,1은 긍정

if result == "0":
  print("부정적인 글입니다")
else:
  print("긍정적인 글입니다")

"""
fontpath = "c:/Windows/Fonts/malgun.ttf"
from wordcloud import WordCloud
cloud = WordCloud(font_path=fontpath, background_color="white", width=510, height=393, max_words=20000, max_font_size=300).generate(" ".join(mergedTextList))
plt.imshow(cloud, interpolation='bilinear') # 글자를 더 부드럽게 나오게 한다
plt.axis('off') # 축의 위치 정보 off
#plt.show()
cloud.to_file('my_first_wordcloud.jpg')
"""
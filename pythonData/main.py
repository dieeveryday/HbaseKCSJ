#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from pyecharts.charts import Page  # 导入Page库
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import jieba  # 中文分词库，自动识别句子里面的中文单词
from nltk import FreqDist  # 使用nltk库统计中文词语出现的频率
from pyecharts.charts import WordCloud

# 数据的读取
data = pd.read_csv("rawData.csv", encoding='utf-8')

# 按照评分人数对数据进行排序，并选取前10个作为绘制对象
df = data.sort_values(by='评分人数', ascending=False).iloc[:10]

# 绘制柱状图
bar = Bar(init_opts=opts.InitOpts(width='800px', height='400px'))  # 设置画布大小

bar.add_xaxis(df['电影名称'].tolist())
bar.add_yaxis('评分人数', df['评分人数'].tolist(),
              itemstyle_opts={'color': '#1E90FF'})  # 设置柱状图颜色

bar.set_global_opts(
    title_opts=opts.TitleOpts(title='电影评价人数', pos_left='left',
                              title_textstyle_opts=opts.TextStyleOpts(font_size = 16)),  # 设置标题位置及样式
    xaxis_opts=opts.AxisOpts(name='片名', axislabel_opts={'rotate': 20, 'interval': 0}),  # 设置x轴标签倾斜角度和间隔
    yaxis_opts=opts.AxisOpts(name='人数', name_gap=30, axislabel_opts=opts.LabelOpts(font_size=14)),
    datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_='inside')],  # 添加滚动条
    toolbox_opts=opts.ToolboxOpts(orient='vertical',
                                  pos_top='middle',
                                  pos_left='right',
                                  feature=opts.ToolBoxFeatureOpts(save_as_image=None,
                                                                  data_view=None,
                                                                  magic_type=None,
                                                                  brush=None)),  # 设置工具箱位置及样式
).set_colors(['#1E90FF'])

# 按照评分对数据进行分组计数，并按照评分进行升序排序
count_by_rating = data.groupby(['电影评分'])['电影名称'].count().sort_index()

# 定义饼图颜色
colors = ['#1980C0', '#4EB3D3', '#7AC2D6', '#A3B1CF', '#BFA0BE',
          '#D68AA0', '#E67377', '#EE4F5F', '#F42955', '#FF0000']

# 设置全局样式
global_style = {
    'legend': {
        'type': 'scroll',
        'orient': 'vertical',
        'right': '3%',
        'top': '20%',
        'itemWidth': 16,
        'itemHeight': 16,
        'textStyle': {'color': '#333', 'fontSize': 14},
        'backgroundColor': 'rgba(0,0,0,0.5)',
        'borderRadius': 4,
        'padding': 10,
    },
    'series': {
        'label': {'formatter': '{b}\n{d:.2f}%'},
    },
    'toolbox': {
        'orient': 'vertical',
        'top': 'middle',
        'right': '3%',
    },
}

# 绘制饼状图
num = count_by_rating.tolist()
lab = count_by_rating.index.tolist()
pie = (
    Pie(init_opts=opts.InitOpts(width='800px', height='600px'))
    .add(series_name='', data_pair=[(i, j) for i, j in zip(lab, num)])
    .set_colors(colors)  # 设置饼图颜色
    .set_global_opts(
        title_opts=opts.TitleOpts(title="电影评分分布", pos_top=None, pos_left="left"),
    )
)

country_all = data['类型'].str.replace(",", " ").str.split(" ", expand=True)
country_all = country_all.apply(pd.value_counts).fillna(0).astype("int")
country_all['count'] = country_all.apply(lambda x: x.sum(), axis=1)
country_all.sort_values('count', ascending=False)
data2 = country_all['count'].sort_values(ascending=False).head(10)

country_counts = data2
country_counts.columns = ['类型', '数量']
country_counts = country_counts.sort_values(ascending=True)
bar2 = (
    Bar(init_opts=opts.InitOpts(width='800px', height='400px'))
    .add_xaxis(list(country_counts.index)[-10:])
    .add_yaxis('影片类型数量', country_counts.values.tolist()[-10:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='影片类型数量', pos_left='left',
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=16)),
        yaxis_opts=opts.AxisOpts(name='类型'),
        xaxis_opts=opts.AxisOpts(name='数量'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)

country_all = data['国家'].str.replace(",", " ").str.split(" ", expand=True)
country_all = country_all.apply(pd.value_counts).fillna(0).astype("int")
country_all['count'] = country_all.apply(lambda x: x.sum(), axis=1)
country_all.sort_values('count', ascending=False)
data1 = country_all['count'].sort_values(ascending=False).head(10)

country_counts = data1
country_counts.columns = ['国家', '数量']
country_counts = country_counts.sort_values(ascending=True)

bar3 = (
    Bar(init_opts=opts.InitOpts(width='800px', height='400px'))
    .add_xaxis(list(country_counts.index)[-10:])
    .add_yaxis('地区上映数量', country_counts.values.tolist()[-10:])
    .reversal_axis()
    .set_global_opts(
        title_opts=opts.TitleOpts(title='地区上映电影数量', pos_left='left',
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=16)),
        yaxis_opts=opts.AxisOpts(name='国家'),
        xaxis_opts=opts.AxisOpts(name='上映数量'),
    )
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
)

# 词云图
# 数据清洗操作:删除重复操作
data = data.drop_duplicates()
# 读取电影名称那一列的数据，转换为字符串类型
com_str = str(data["电影名称"].values)
# print(com_str)
cut_words = jieba.lcut(com_str)
# print(cut_words)

freq_list = FreqDist(cut_words)
# print(freq_list)
most_common_words = freq_list.most_common()
# print(most_common_words)

# 词云图的绘制
w = (
    WordCloud(init_opts=opts.InitOpts(width='800px', height='400px'))
    .add("", most_common_words, word_size_range=[15, 20])
    .set_global_opts(title_opts=opts.TitleOpts(title="电影名称WordCloudPicture",
                                               pos_left='left',
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=16)),
                     )
)

page = Page(layout=Page.SimplePageLayout)
page.add(pie, bar, bar2, bar3, w)
page.render("result.html")

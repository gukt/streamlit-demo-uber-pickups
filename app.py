import datetime
import streamlit as st
import pandas as pd
import numpy as np

# 每个应用都有一个标题，我们设置一个标题
# 这个不是显示在标题栏上的，而是显示在页面顶部的标题
st.title('Uber pickups in NYC')



DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# 每次运行应用时，如果我们都会重新加载数据，那么这将非常慢。
# 添加 @st.cache_data 会让 Streamlit 缓存数据，
# 这样我们就不必每次运行应用时都重新加载数据。
# Streamlit 会检测数据是否发生变化，如果发生变化，它会重新加载数据。
# 检测的依据有两条：
# 1. 如果输入参数发生变化
# 2. 如果函数的实现发生变化
#   # 哪怕是改变打印输入值，也表示函数的实现发生了变化，例如：
#   # print('222') 改为 print('333')
@st.cache_data
def load_data(nrows):
  # 下载数据，并放到 Pandas 的 DataFrame 中
  data = pd.read_csv(DATA_URL, nrows=nrows)
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)
  # 将日期字符串转换为日期对象
  data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
  return data

# 创建一个文本元素，提示我们正在加载数据
data_load_state = st.text('Loading data...')
# 加载 10,000 行数据
data = load_data(10000)
# 现在，我们已经加载了数据，我们在文本元素中显示“加载数据...完成！”
data_load_state.text('Done! (using st.cache_data)')

# 这样就可以输出到页面上了
# data

# 但我们也可以通过 write() 方法来输出
# st.subheader('Raw data')
# st.write(data)

# 使用 checkbox 来控制是否显示原始数据
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# 也可以通过 dataframes() 方法来输出
# st.dataframe(data)

# write 方法可以输出各种类型的数据
st.write(1,2,3)
st.write('Hello Streamlit')
st.write(True)
# st.write(datetime.now())
st.write('hello'
        ' world'
        ' # Markdown 支持不支持？')

# 下面绘制一个图表（直方图）
st.subheader('Number of pickups by hour')
# Generate a histogram that breaks down pickup times binned by hour
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# Draw this histogram
st.bar_chart(hist_values)

# 下面绘制一个地图并标注数据
st.subheader('Map of all pickups')
st.map(data)

# 过滤地图显示数据
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# 添加一个滑动条，让用户可以选择要显示的时间
st.subheader('添加一个滑动条，让用户可以选择要显示的时间')
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)








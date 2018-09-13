
# coding: utf-8

# In[201]:


import numpy as np
import pandas as pd
import json

path = 'E:\数据挖掘学习\zufang1.txt'
#读取文件
content = [json.loads(line) for line in open(path,encoding='utf-8')]
df = pd.DataFrame(content)
df.info()


# In[202]:


#空值处理
df = df.applymap(lambda e: np.nan if e== 'null' else e)


# In[203]:


#去掉重复的数据
df= df.drop_duplicates()
#去掉指定栏位的重复的数据
df = df.drop_duplicates(['url'])


# In[204]:


df.url.value_counts()


# In[205]:


#查看各个栏位缺失值数量
df.isnull().sum()


# In[206]:


#舍弃缺失值
df = df.dropna(thresh=5)
df.isnull().sum()


# In[207]:


#查看缺失值
df[df.isnull().values==True]


# In[208]:


#数据清洗处理
def change(s):
    if '平米'in s: 
        return s.split('平米')[0] 
    else: 
        return s
df['acreage'] = df['acreage'].map(change)


# In[209]:


#类型转换
df['rent'] = df['rent'].astype(np.float64)
df['acreage'] = df['acreage'].astype(np.float64)
df.head()


# In[210]:


#选取合租的平均值填充
hezu = df[~df['rentstyle'].isin(['整租'])]
df['rent'].fillna(hezu.groupby(['pattern'])['rent'].transform('mean'),inplace=True)


# In[211]:


#缺失值填充
df = df.fillna(0)


# In[212]:


df.sort_values(by='rent',ascending=False)


# In[213]:


#筛选租金去除异常值上限和下限
data = df[(df['rent']< 5000) & (df['rent']>200)]


# In[214]:


#数据整理
data['均价'] = data['rent']/data['acreage']
data = data.round({'均价':2})
data = data.round({'rent':2})
data = data[['rent','均价','acreage','score','pattern','decorate','rentstyle','address','url']]


# In[215]:


data[['室','厅','卫']] = df['pattern'].str.extract('(\d+)室(\d+)厅(\d+)')
data[['室','厅']] = df['pattern'].str.extract('(\d+)室(\d+)厅')
data = data.fillna(0)


# In[218]:


#根据上班地点和自身条件，重新给房源评分，最终找到适合自己的房源
def my_acreage(s):
    num = 0
    if s>40:
        num+=1
        return num
    else:
        return num
data['面积评分'] = data['acreage'].map(my_acreage)

def my_rent(s):
    num = 0
    if s<2000:
        num+=1
        return num
    return num
data['租金评分'] = data['rent'].map(my_rent)

def my_decorate(s):
    num = 0
    if s in ['精装修','豪华装修']:
        num+=1
        return num
    return num
data['装修评分'] = data['decorate'].map(my_decorate)

def my_addres(s):
    num = 0
    if '龙华' in s:
        return 2
    if '南山' in s:
        return 1
    return num
data['地址评分'] = data['address'].map(my_addres)

data['总评分'] = data['面积评分']+data['租金评分']+data['装修评分']+data['地址评分']
my_data = data.rename(columns={'rent':'租金(元)','acreage':'面积(平米)','score':'评分','rentstyle':'出租方式','decorate':'装修','address':'地址','pattern':'户型'})

my_data = my_data.sort_values(by='总评分',ascending=False)
my_data = my_data[['租金(元)','面积(平米)','均价','评分','户型','室','厅','卫','装修','出租方式','面积评分','租金评分','装修评分','地址评分','总评分','地址','url']]
my_data.head(20)
my_data.to_csv('E:\数据挖掘学习\zufang1.csv',index=False)

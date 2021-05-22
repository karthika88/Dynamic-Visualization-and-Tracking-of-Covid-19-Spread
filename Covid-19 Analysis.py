#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import requests
from pandas.io.json import json_normalize
api_url='https://covid.ourworldindata.org/data/owid-covid-data.json'
jsonData = requests.get(api_url) # (your url)
data = jsonData.json()


# In[2]:


data.keys()


# In[3]:


data['AFG']['location']


# In[4]:


info_per_country=list(data['AFG'].keys())
info_per_country.remove('data')


# In[5]:


info_per_country


# In[6]:


for each_info in info_per_country:
  try:
    print(each_info,': ',data['USA'][each_info])
  except KeyError:
    print(each_info,': ', 'Nan')


# In[7]:


df=pd.DataFrame()
data_df=pd.DataFrame()
country_list=data.keys()  # For getting data of all countries use data.keys()
info_per_country=list(data['AFG'].keys())
info_per_country.remove('data')

for country in country_list:
  df=pd.json_normalize(data[country]['data'])
  df['country_code']=country
  for entry in info_per_country:
    try:
      df[entry]=data[country][entry]
    except KeyError:
      df[entry]='Nan'


  data_df = pd.concat([data_df, df], axis=0)  


# In[8]:


data_df.head()


# In[9]:


rearranged_cols=['country_code']+info_per_country
present_cols=list(data_df.columns)


# In[10]:


end_index=present_cols.index('country_code')
remaining_cols=present_cols[0:23]


# In[11]:


remaining_cols


# In[12]:


rearranged_cols=rearranged_cols+remaining_cols


# In[13]:


rearranged_cols


# In[14]:


data_df=data_df[rearranged_cols]


# In[15]:


data_df


# In[16]:


# choropleth map using plotly
import plotly.graph_objs as go 
from plotly.offline import init_notebook_mode,iplot,plot
init_notebook_mode(connected=True) 


# In[21]:


data = dict(type='choropleth',
            colorscale = 'Viridis',
            reversescale = True,
            locations = data_df['location'],
            z = data_df['people_fully_vaccinated'],
            locationmode = 'country names',
            text = data_df['country_code'],
            marker = dict(line = dict(color = 'rgb(100,100,150)',width = 1)),
            colorbar = {'title':"Covid-19 Vaccination Progress"}
            ) 


# In[24]:


layout = dict(title = 'Covid-19 Analysis',
              geo = dict(scope='world',
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)')
             )


# In[26]:


choromap = go.Figure(data = [data],layout = layout)
plot(choromap,validate=False)


# In[ ]:





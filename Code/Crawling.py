#!/usr/bin/env python
# coding: utf-8

# In[27]:


import time
import requests
import pandas as pd
import numpy as np

from tqdm import tqdm


# In[28]:


pat_num = pd.read_csv('./data/final_health_care_patent.csv', encoding='utf8')
pat_nums = [i.split('-')[1] for i in pat_num['id']]


# In[29]:


url_post = 'https://api.patentsview.org/patents/query'
post_len = 10000

# Crawling elements
f = '&f=["patent_number","patent_title","patent_date", ''"patent_type","patent_abstract","cpc_subgroup_id", ''"assignee_id", "assignee_total_num_patents", "cpc_total_num_assignees", ''"cited_patent_number", "citedby_patent_number", ''"examiner_id", "examiner_role", "examiner_group"]'


# In[30]:


pt_dict_list=[]
st = time.time()
for n, i in enumerate(tqdm(pat_nums)):
    q1 = '?q={"patent_number":'
    q2 = '}'
    q = q1 + '"' + i + '"' + q2
    
    t_data = q + f
    t_post = requests.get(url_post + t_data)
    
    while '500' in str(t_post):
        t_post = requests.get(url_post + t_data)
    try:
        t_json = t_post.json()
    except:
        continue
        
    try:
        pt_dict_list.extend(t_json['patents'])
    except TypeError:
        pass
    
#     if n%10 == 0:
#         print(n / 10)
        
print('Time spending', time.time() - st)


# In[31]:


# filtering by patent type (we need utility type patent only!!)
util_patent = [i for i in pt_dict_list if i['patent_type'] == 'utility']


# In[32]:


print(util_patent[0])


# In[33]:


# CPC to list
for d in util_patent:
    cpc_set = ''
    for c in d['cpcs']:
        try:
            cpc = c['cpc_subgroup_id'].split('/')[0]
            cpc_set = cpc_set + ',' + cpc
        except:
            cpc_set = cpc_set + 'None'
    d['cpc_set'] = cpc_set


# In[34]:


print(util_patent[0])


# In[35]:


# dict to dataframe
df = pd.DataFrame.from_dict(util_patent).drop(['cpcs'], axis=1)
df.drop_duplicates(['patent_abstract'], inplace=True)
print('Patent list length: ', len(df))


# In[36]:


# CSV로 저장
df.to_csv('./data/final_patent.csv', encoding='utf8', index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





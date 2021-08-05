#!/usr/bin/env python
# coding: utf-8


import time
import requests
import pandas as pd
import numpy as np

from tqdm import tqdm


# 특허파일 읽어오기
# 특허파일은 google patent advanced search에서 다운받음
pat_num = pd.read_csv('./data/final_health_care_patent.csv', encoding='utf8')
pat_nums = [i.split('-')[1] for i in pat_num['id']]


# api 긁어올 주소 설정
url_post = 'https://api.patentsview.org/patents/query'
post_len = 10000

# Crawling elements
f = '&f=["patent_number","patent_title","patent_date", ''"patent_type","patent_abstract","cpc_subgroup_id", ''"assignee_id", "assignee_total_num_patents", "cpc_total_num_assignees", ''"cited_patent_number", "cited_patent_date", "citedby_patent_number", "citedby_patent_date", ''"examiner_id", "examiner_role", "examiner_group"]'


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
    
print('Time spending', time.time() - st)


# filtering by patent type (we need utility type patent only!!)
util_patent = [i for i in pt_dict_list if i['patent_type'] == 'utility']

# util_patent의 형태 확인
print(util_patent[0])


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

    
# dict to dataframe
df = pd.DataFrame.from_dict(util_patent).drop(['cpcs'], axis=1)
df.drop_duplicates(['patent_abstract'], inplace=True)
print('Patent list length: ', len(df))


# CSV로 저장
df.to_csv('./data/final_patent.csv', encoding='utf8', index=False)
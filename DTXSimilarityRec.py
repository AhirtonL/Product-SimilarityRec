#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
__author__ = "Ahirton Lopes"
__copyright__ = "Copyright 2018, Duratex"
__credits__ = ["Ahirton Lopes"]
__license__ = "None"
__version__ = "1.0"
__maintainer__ = "Ahirton Lopes"
__email__ = "ahirtonlopes@gmail.com"
__status__ = "Beta"
""""

import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

ds = pd.read_csv("TestePortfolio.csv")

my_stopword_list = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j',
          'k','l','ç','z','x','c','v','b','n','m','Q','W','E','R','T','Y','U',
          'I','O','P','A','S','D','F','G','H','J','K','L','Ç','Z','X','C','V',
          'B','N','M','!','@','#','$','%','¨','&','*','(',')','_','+','-','--','=',
          '´','`','^','~',':',';','?','|','{','[','}','<','>','.',',','/','//','...',
          '"',"'","''",'``','no', 'na', 'do', 'da', 'de', 'as', 'os', 'nos', 'nas', 
          'dos', 'das', 'se', 'em','para','que','pela','pelo', 'com','sem', 'c/', 's/',
          'um','uma','pra',' ', 'aos', 'etc', 'e/ou', 'ou','ate','por','como', 'ao',
          'nao','mais','maior','menor','tambem', 'ja',
          'ele','ela','aquilo','aquele','aquela','isso','esse','essa','este','esta',
          'sua','seu', 'neste', 'nesta', 'nesse', 'nessa',
          'algum','alguma','alguns','algumas', 'porque','por que', 'nem', 'rt', 'me', 'http', 'https']

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words= my_stopword_list)
tfidf_matrix = tf.fit_transform(ds['description'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    # Remocao do primeiro item
    # Cada entrada no dicionario representa um item na forma (rating, item_id)
    
    results[row['id']] = similar_items[1:]
    
    #print results
        
#print('Resultados ok!')

# Dado um ID tem-se a descricao (informacoes concatenadas do item)

def item(id):
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0]
    #print ds

# Leitura dos resultados recomendados via dicionario e output de recomendacoes

def recommend(item_id, num):
    recs = results[item_id][:num]
    
    # Dataframe append 
    df_result = pd.DataFrame(columns=['id_produto','id_produto_recomendado','similaridade'])
    
    # Processa recomendação para cada produto
df_result = pd.DataFrame(columns=['id_produto','id_produto_recomendado','similaridade'])

for index,row in ds.iterrows():
    df_result = df_result.append(recommend(item_id=row['id'], num=10),ignore_index = True)
    print df_result
    for rec in recs:

        r2 = {'id_produto':item_id, 'id_produto_recomendado': rec[1],'similaridade': str(rec[0])}
        #salva resultado dataframe
        df_r2 = pd.DataFrame([r2])
        
        #append do resultado
        df_result = df_result.append(df_r2,ignore_index = True)
        
    return df_result

# Processa recomendação para cada produto
df_result = pd.DataFrame(columns=['id_produto','id_produto_recomendado','similaridade'])

for index,row in ds.iterrows():
    df_result = df_result.append(recommend(item_id=row['id'], num=10),ignore_index = True)
    print df_result
    
# Exporta csv
df_result.to_csv("Desktop/recomendacao.csv",index  = False)
    
    
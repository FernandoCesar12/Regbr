#!/usr/bin/env python
# coding: utf-8

# # Removendo a limitação do número de linhas

# In[1]:


import sys
import csv
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


# # Realizando a importação da base de dados

# In[2]:


import pandas as pd

df_1 = pd.read_csv('Portaria_anac_parte1.txt', sep = '汉')
df_2 = pd.read_csv('Portaria_anac_parte2.txt', sep = '汉')
df_3 = pd.read_csv('Portaria_anac_parte3.txt', sep = '汉')
df_4 = pd.read_csv('Portaria_anac_parte4.txt', sep = '汉')
df_5 = pd.read_csv('Portaria_anac_parte5.txt', sep = '汉')
df_6 = pd.read_csv('Portaria_anac_parte6.txt', sep = '汉')
df_7 = pd.read_csv('Portaria_anac_parte7.txt', sep = '汉')
df_8 = pd.read_csv('Portaria_anac_parte8.txt', sep = '汉')


# # Juntando os Dataframes 

# In[3]:


dados_1 = pd.concat([df_1,df_2])
dados_2 = pd.concat([dados_1,df_3])
dados_3 = pd.concat([dados_2,df_4])
dados_4 = pd.concat([dados_3,df_5])
dados_5 = pd.concat([dados_4,df_6])
dados_6 = pd.concat([dados_5,df_7])
dados_7 = pd.concat([dados_6,df_8])


# In[4]:


dados_7[dados_7['Texto_lei'].map(len) < 5]


# # Removendo os links corrompidos

# In[5]:


df = dados_7[dados_7['Texto_lei'].map(len) >= 5]


# # Exportando os resultados

# In[6]:


df.to_csv("Portaria_anac.txt", index=False, encoding='utf-8-sig', sep = '汉')


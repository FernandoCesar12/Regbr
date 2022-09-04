#!/usr/bin/env python
# coding: utf-8

# # Instrução normativa

# In[1]:


#pip install selenium

#!apt install chromium-chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = "http://www.ans.gov.br/legislacao/legislacaobusca-de-legislacao?temaId=&diretoriaId=&relevancia=Relevancia&assuntoId=&normaId=8&numero=&revogada=1&palavra_chave=&publicacao=Igual+a&data_dou=&acao=buscar&limit=0&option=com_legislacao&origin=aHR0cDovL3d3dy5hbnMuZ292LmJyL2xlZ2lzbGFjYW8vYnVzY2EtZGUtbGVnaXNsYWNhbw05d616f62b90da199f7fa97cc28c531frpfuql736qe23i8lob7mdle2v1&post=legislacaobusca-de-legislacao&view=legislacao"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)
time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'lxml')
Conteudo = soup.find_all('div', class_='table-responsive')
Texto = ' '.join([str(elem) for elem in Conteudo]).split('</a>')
       
href = []

for i in range(0,len(Texto)):
    if 'class="btn btn-primary"' in Texto[i]:
        result = Texto[i].split('class="btn btn-primary" href="')[1].split('" target="_blank">')[0].replace('amp;','')
        href.append(result)
            
append_str = 'http://www.ans.gov.br'
Link_lista = [append_str + sub for sub in href]


# ### Extraindo os textos via HTML

# In[3]:


import requests # requisições web
import re
from bs4 import BeautifulSoup

url_list = Link_lista

Texto_lista = []
for url in url_list:
    
    try:
        
        header = {'User-Agent': "'Mozilla/5.0'"}
        html = requests.get(url, headers = header)
        bs_obj = BeautifulSoup(html.text,"lxml").text
        texto = bs_obj.replace('\n','').replace('\xa0','').replace('\t','').replace('  ','')
        Texto_lista.append(texto)
        
    except:
        print('Url vazia')


# ### Criando o DataFrame

# In[6]:


# Separando as datas das resoluções
    
Data_lei = []

pattern = r"\d+ [DE]*[de]* [JANEIRO]*[FEVEREIRO]*[MARÇO]*[ABRIL]*[MAIO]*[JUNHO]*[JULHO]*[AGOSTO]*[SETEMBRO]*[OUTUBRO]*[NOVEMBRO]*[DEZEMRBO]*[]* [DE]*[de]* \d+"

for i in range(0,len(Texto_lista)):
    result = re.search(pattern, Texto_lista[i])
    
    if result != None:
        Data_lei.append(str(result).split("match='")[1].split("'>")[0]) # Serve para verificar se a lei foi revogada
    else:
        Data_lei.append('0000')
        
Ano_lei = []
for i in range(0,len(Data_lei)):

    result = str(Data_lei[i]).replace('.','').replace(',','').replace('[','').replace(']','').replace('"','').replace("'","")[-4:]
    Ano_lei.append(result)
    
ano_list = []
for i in range(0,len(Ano_lei)):
    if len(Ano_lei[i].replace(' ','').replace('.','').replace('[','').replace(']','')) != 4:
        result = '0000'
        ano_list.append(result)
    else:
        result = Ano_lei[i]
        ano_list.append(result)
    
    
Num_lei_1 = []

for j in range(0,len(Texto_lista)):
    if 'Nº' in str(Texto_lista[j]):
        result = str(Texto_lista[j]).split('Nº')[1].split(',')[0]
        Num_lei_1.append(result)
    elif 'N°' in str(Texto_lista[j]):
        result = str(Texto_lista[j]).split('N°')[1].split(',')[0]
        Num_lei_1.append(result)
    else:
        Num_lei_1.append('000')
        
Num_lei = []

for j in range(0,len(Num_lei_1)):
    if 'DE' in str(Num_lei_1[j]) and ':' not in str(Num_lei_1[j]):
        result = str(Num_lei_1[j]).split('DE')[0].replace(' ','').replace('foialteradapela','').replace('-','')
        Num_lei.append(result)
    
    elif ':' in str(Num_lei_1[j]):
        result = str(Num_lei_1[j]).split(':')[0].replace(' ','').replace('foialteradapela','').replace('-','')
        Num_lei.append(result)
        
    else:
        Num_lei.append(Num_lei_1[j].replace(' ','').replace('foialteradapela','').replace('-',''))
        
Num_lei_2 = []

for j in range(0,len(Num_lei)):
    if len(str(Num_lei[j])) > 10:
        result = str(Num_lei[j])[0:2]
        Num_lei_2.append(result)
    else:
        Num_lei_2.append(Num_lei[j])
        
# Criando o ID

Tipo = ['1008']*len(Texto_lista) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano_list)] 


# Separando se a resolução foi revogada
    
Revogada = []

for i in range(0,len(Texto_lista)):
    if 'Revogada' in Texto_lista[i] or 'REVOGADA' in Texto_lista[i] or 'revogada' in Texto_lista[i]:
        result = True
        Revogada.append(result)
    
    else:
        result = False
        Revogada.append(result)

import pandas as pd
import numpy as np

# Criando um DataFrame para alocar os outputs

dados = pd.DataFrame (ID ,columns=['ID'])
dados['Texto_lei'] = Texto_lista
dados['Data_lei'] = Data_lei
dados['Data_publicação'] = ['']*len(Texto_lista)
dados['Tipo_lei'] = Tipo
dados['Revogada'] = Revogada
dados['Setor'] = ['ANAC']*len(Texto_lista)

dados['Texto_lei'].replace('', np.nan, inplace=True)
dados.dropna(subset=['Texto_lei'], inplace=True)


# In[7]:


dados


# In[34]:


# Exportando o banco de dados

dados.to_csv("Sumula_ANS.txt", index=False, encoding='utf-8-sig', sep = '汉')


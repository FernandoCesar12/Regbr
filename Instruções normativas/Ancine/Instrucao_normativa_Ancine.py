#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das instruções normativas

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

url = "https://www.gov.br/ancine/pt-br/acesso-a-informacao/legislacao/instrucoes-normativas"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)
        
soup = BeautifulSoup(driver.page_source, 'lxml')

texto = ' '.join([str(elem) for elem in soup]).split('data-tippreview-image=""')

conteudo_textual = []

for i in range(0,len(texto)):
    if 'data-tippreview-title="" href="' in str(texto[i]):
        result = str(texto[i]).split('data-tippreview-title="" href="')[1].split('" target="')[0]
        conteudo_textual.append(result)
        
links = list(dict.fromkeys(conteudo_textual))


# # Pegando o conteudo textual dos links HTML

# In[23]:


#pip install selenium

#!apt install chromium-chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re
import time

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

# Separando os links que não estão em pdf

link_html = []

for i in range(0,len(links)):
    if '.pdf' not in str(links[i]) and '.doc' not in str(conteudo_textual[i]) and '.xlsx' not in str(conteudo_textual[i]):
        link_html.append(links[i])
        
for i in range(0,len(link_html)):
    if '" style="' in str(link_html[i]):
        link_html[i] = str(link_html[i]).split('" style="')[0]
        
url_list = link_html

titulo_html = []
texto_html = []

for url in url_list:
    if '.htm' not in str(url):
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        titulo_html.append(str(soup.find_all('h1', class_='documentFirstHeading')).split('<h1 class="documentFirstHeading">')[1].split('</h1>')[0])
        texto_html.append(re.sub('<[^>]+>', '', str(soup.find_all('div', id='content-core'))))
        
    elif '.htm' in str(url):
        

        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
            
        if 'rgb(' in str(soup) and 'color="#000080" face="Arial">' not in str(soup):
            titulo_html.append(re.sub('<[^>]+>', '', str(soup).split('rgb(')[1].split('</a>')[0].replace('\n','').replace('  ','')))
            texto_html.append(re.sub('<[^>]+>', '', str(soup).replace('\n','')))
            
        elif 'color="#000080" face="Arial">' in str(soup):
            titulo_html.append(re.sub('<[^>]+>', '', str(soup).split('color="#000080" face="Arial">')[1].split('</a>')[0].replace('\n','').replace('  ','').replace(' face="Arial">','')))
            texto_html.append(re.sub('<[^>]+>', '', str(soup).replace('\n','')))
                
        else:
            titulo_html.append('')
            texto_html.append('')    
            
Titulo = []
for i in range(0,len(titulo_html)):
    if '0,0,128)">' in str(titulo_html[i]):
        Titulo.append(str(titulo_html[i]).split('0,0,128)">')[1])
    else: 
        Titulo.append(str(titulo_html[i]))


# In[82]:


# Separando as datas das resoluções
                  
Ano_lei = []
for i in range(0,len(Titulo)):

    result = str(Titulo[i]).replace(' ','').replace('.','')[-4:]
    Ano_lei.append(result)
    
    
Num_lei = []

for i in range(0,len(Titulo)):
    
    if 'LEI' not in str(Titulo[i]).upper():

        result = str(Titulo[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').split('Nº')[1].split(' ',2)[1].replace(' ','').replace(',','').replace('.','').replace('-','')
        Num_lei.append(result)
        
    else:
        
        result = str(Titulo[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').replace('NO','Nº').split('Nº')[1].split(' ',2)[1].replace(' ','').replace(',','').replace('.','').replace('-','')
        Num_lei.append(result)
        
Num_lei_2 = []

for i in range(0,len(Num_lei)):
    if len(str(Num_lei[i])) <1:
        Num_lei_2.append('000')
    else:
        Num_lei_2.append(str(Num_lei[i]))
        
# Criando o ID

Tipo = ['710']*len(Titulo) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei_2)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei)] 

# Separando a data de publicação no DOU
    
Data_lei = []

for i in range(0,len(Titulo)):
    
    if 'LEI' not in str(Titulo[i]).upper():

        result = str(Titulo[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').split('Nº')[1].split(' ',3)[3].replace(',','').replace('.','').replace('-','')
        Data_lei.append(result)
        
    else:
        
        result = str(Titulo[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').replace('NO','Nº').split('Nº')[1].split(' ',3)[3].replace(',','').replace('.','').replace('-','')
        Data_lei.append(result)
        
# Separando se a resolução foi revogada
    
Revogada = []

for i in range(0,len(Titulo)):
    if 'Revogada' in Titulo[i] or 'REVOGADA' in Titulo[i] or 'revogada' in Titulo[i]:
        result = True
        Revogada.append(result)
    
    else:
        result = False
        Revogada.append(result)


# # Visualizando as variáveis do Banco de Dados Brutos

# In[85]:


import pandas as pd
import numpy as np

# Criando um DataFrame para alocar os outputs

BANCO = pd.DataFrame (ID ,columns=['ID'])
BANCO['Texto_lei'] = Titulo
BANCO['Data_lei'] = Data_lei
BANCO['Data_publicação'] = Data_lei
BANCO['Tipo_lei'] = Tipo
BANCO['Revogada'] = Revogada
BANCO['Setor'] = ['ANCINE']*len(Titulo)

BANCO


# # Exportando a base de dados

# In[86]:


import pandas as pd 

BANCO = pd.DataFrame (links ,columns=['Links'])
BANCO.to_csv("Instrucao_normativa_Ancine.txt", index=False, encoding='utf-8-sig', sep = '汉')


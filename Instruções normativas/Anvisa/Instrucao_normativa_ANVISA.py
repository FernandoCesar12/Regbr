#!/usr/bin/env python
# coding: utf-8

# # Pegando os primeiros links

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

url = "http://antigo.anvisa.gov.br/legislacao#/"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)
time.sleep(10)

# Remover na hora de rodar oficialmente

# Apertando o botão de buscar

driver.find_element_by_xpath('//*[@id="p_p_id_legislacao_WAR_etapasregulatoriasportlet_"]/div/div/div/div/div/div[2]/div[2]/fieldset/p/input').click();
time.sleep(5)

# Apertando os filtros de Portaria

driver.find_element_by_xpath('//*[@id="p_p_id_legislacao_WAR_etapasregulatoriasportlet_"]/div/div/div/div/div/div[2]/div[2]/fieldset/ul/li[5]/input').click();
time.sleep(5)

driver.find_element_by_xpath('//*[@id="p_p_id_legislacao_WAR_etapasregulatoriasportlet_"]/div/div/div/div/div/div[2]/div[2]/fieldset/ul/li[6]/input').click();
time.sleep(5)


Conteudo_lista = []

j = 0

while j <= 22:
    
    try:
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        Conteudo = soup.find_all('a', class_='ng-binding')
        texto = ' '.join([str(elem) for elem in Conteudo]).split('</a>')
    
        Lista_rotulo = []
        for i in range(0,len(texto)-1):
            if '#/visualizar' in texto[i]:
                result = texto[i].split('href="')[1].split('" ui')[0]
                Lista_rotulo.append(result)
        
        Conteudo_lista.append(Lista_rotulo)
        
        driver.find_element_by_xpath('//*[@id="p_p_id_legislacao_WAR_etapasregulatoriasportlet_"]/div/div/div/div/div/div[3]/dir-pagination-controls/div/ul/li[11]/a').click();
        time.sleep(3)
        
        j = j+1
        
    except:
        break
        
Lista = [item for sublist in Conteudo_lista for item in sublist]

append_str = 'http://antigo.anvisa.gov.br/legislacao'
Link_lista = [append_str + sub for sub in Lista]


# # Pegando os links para os PDF's

# In[4]:


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url_list = Link_lista
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

link_PDF = []

for url in url_list:
    
    driver.get(url)

    driver.implicitly_wait(30)
    time.sleep(10)

    html = driver.page_source
    
    if html.count('/documents') == 2:
        
        conteudo = html.split('/documents',2)[2].split('class="ng-scope"')[0].replace('"','').replace(' ','')
        link_PDF.append(conteudo)

append_str = 'http://antigo.anvisa.gov.br/documents'
Link_lista = [append_str + sub for sub in link_PDF]

Link_lista_final = []
for k in range(0,len(Link_lista)):
    if len(Link_lista[k])< 200:
        result = Link_lista[k]
        Link_lista_final.append(result)


# # Realizando a leitura dos PDF's

# In[6]:


# Entrando com os pacotes necessários

import io
import requests
from PyPDF2 import PdfFileReader


#Selecionando a URL

url_list = Link_lista_final

Texto = []

for url in url_list:

    try:
        
        # Lendo o conteudo presente no PDF

        r = requests.get(url)
        f = io.BytesIO(r.content)

        reader = PdfFileReader(f)

        content = [] # Realizando o loop para pegar todas as páginas simultaneamente
        for page in range(0,reader.numPages):
            content.append(reader.getPage(page).extractText()) 

        # Realizando limpeza e manipulação do texto em PDF

        listToStr = ' '.join([str(elem) for elem in content]).replace('\n','') # Transformando a lista em String
        Texto.append(listToStr)
        
    except:
        Texto.append('')
        
# Separando algumas informações 

Titulo = []
for i in range(0,len(Texto)):
    if 'INSTRUÇÃO NORMATIVA' in Texto[i]:
        result = Texto[i].replace('Nº','N°').replace('Nª','N°').split('N°')[1].split('(Publicada')[0]
        Titulo.append('INSTRUÇÃO NORMATIVA' + result)
    else:
        Titulo.append('')
        
Titulo_2 = []
for i in range(0,len(Titulo)):
    if 'ISSN' in str(Titulo[i]):
        result = str(Titulo[i]).split('ISSN')[0][:-2]
        Titulo_2.append(result)
    else:
        Titulo_2.append(Titulo[i])

        
Info_DOU = []
for i in range(0,len(Texto)):
    if 'Publicada no DOU' in Texto[i]:
        result = Texto[i].split('(Publicada')[1].split(')')[0]
        Info_DOU.append('Publicada' + result)
    
    else:
        result = ''
        Info_DOU.append(result)


# # Separando as informações para criação do DataFrame

# In[80]:


################################################ Criando o ID

import re

Tipo = ['711']*len(Texto) # Tipo de Lei

Ano_lei = []
for i in range(0,len(Titulo_2)):
    if Titulo_2[i] != '':
        result = str(Titulo_2[i]).replace(' ','')[-4:]
        Ano_lei.append(result)
    else:
        result = '0000'
        Ano_lei.append(result)

Num_lei = [] # Pegando o número da lei
for i in range(0,len(Titulo_2)):
    if Titulo_2[i] != '':
        result = Titulo_2[i].split('INSTRUÇÃO NORMATIVA')[1].split(',')[0]
        Num_lei.append(result)
    else:
        Num_lei.append('')

parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei)] 

ID_replace= []
for i in range(0,len(ID)):
    result = ID[i].replace(" ","")
    ID_replace.append(result)
    
################################################ Data_lei

Data = []
for i in range(0,len(Titulo_2)):
    if Titulo_2[i] != '' and 'feira' not in str(Titulo_2[i]):
        result = Titulo_2[i].split(', DE')[1]
        Data.append(result)
        
    elif Titulo_2[i] != '' and 'feira' in str(Titulo_2[i]):
        result = Titulo_2[i].split(',')[2]
        Data.append(result)
    else:
        result = ''
        Data.append(result)
    
################################################ Data_DOU

Data_DOU = []
for i in range(0,len(Info_DOU)):
    if Info_DOU[i] != '':
        result = Info_DOU[i].split(', de')[1]
        Data_DOU.append(result)
    else:
        result = ''
        Data_DOU.append(result)
    
################################################ Revogada

Revogada = []
for i in range(0,len(Texto)):
    if 'Revogada pela Resolução' in Texto[i]:
        result = True
        Revogada.append(result)
    else:
        result = False
        Revogada.append(result)


# # Criando o DataFrame

# In[81]:


import pandas as pd

# Criando um DataFrame para alocar os outputs

BANCO = pd.DataFrame (ID_replace ,columns=['ID'])
BANCO['Texto_lei'] = Texto
BANCO['Data_lei'] = Data
BANCO['Data_publicação'] = Data_DOU
BANCO['Revogada'] = Revogada
BANCO['Tipo_lei'] = Tipo
BANCO['Setor'] = ['ANVISA']*len(Titulo)
BANCO


# In[82]:


# Exportando o banco de dados

BANCO.to_csv("Intrucao_normativa_anvisa.txt", index=False, encoding='utf-8-sig', sep = '汉')


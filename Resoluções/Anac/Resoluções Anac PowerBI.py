#!/usr/bin/env python
# coding: utf-8

# # Importando o banco de dados

# In[28]:


#pip install selenium

#!apt install chromium-chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import time
import re
import os
import requests

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = "https://www.gov.br/anac/pt-br/acesso-a-informacao/participacao-social/governanca-regulatoria/gestao-do-estoque-regulatorio"

pattern = r"https://www.gov.br\/anac\/pt-br\/centrais-de-conteudo\/publicacoes\/arquivos\/tabela-de-controle-dos-atos-normativos"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(20)

######################################### Mudando para o Iframe da página

iframe = driver.find_element_by_xpath('//*[@id="parent-fieldname-text"]/p[4]/iframe')
driver.switch_to.frame(iframe)

time.sleep(5)

bs_obj = BeautifulSoup(driver.page_source, 'lxml')
posicao = str(bs_obj).split('<a')

resolucoes_PDF = []

for href in posicao:
    result = re.search(pattern, str(href))

    if result != None:
        resolucoes_PDF.append(result.group())

link_PDF = list(dict.fromkeys(resolucoes_PDF))
   
print(link_PDF)

dados = pd.read_excel('tabela-de-controle-dos-atos-normativos.xlsx', sheet_name='Resoluções')


# # Separando as informações

# In[25]:


# Separando o ID

ano_list = []
for i in range(0,len(dados['ANO'])):
    ano_list.append(str(dados['ANO'][i]))

Num_lei = []
for i in range(0,len(dados['No da Resolução'])):
    Num_lei.append(str(dados['No da Resolução'][i]))

tipo = ['702']*len(Num_lei)
    
parte1 = [i + j for i, j in zip(tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano_list)] 

revogada = list(dados['Classificação'])

# Conferindo se a resolução foi revogada

lista_revogada = []

for i in range(0,len(revogada)):
    if 'Revogada' in str(revogada[i]):
        lista_revogada.append('True')
    else:
        lista_revogada.append('False')
        
# Data da lei

Data_lei = []

for i in range(0,len(dados['titulo_n'])):
    if ',' in str(dados['titulo_n'][i]):
        Data_lei.append(str(dados['titulo_n'][i]).split(', de')[1])
    else:
        Data_lei.append('')


# # Realizando a Leitura de PDF via HTML

# In[28]:


pip install PyPDF2


# In[43]:


# Entrando com os pacotes necessários

import io
import requests
from PyPDF2 import PdfFileReader

#Selecionando a URL

display = list(dados['Hiperlink_Excel'])
url_list = display

DOU_list = []
Texto_list = []

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

    listToStr = ' '.join([str(elem) for elem in content]) # Transformando a lista em String
    listToStr = listToStr.replace('\n','').replace('  ','').replace('_','')
    listToStr = listToStr.split(".", 2)

    # Separando o título da Resolução e o texto presente no arquivo

    if len(content[0]) >=500:
      if listToStr[0] != ' ':
        if "RESOLUÇÃO" in listToStr[1]:
          Texto = listToStr[2]

        else: 
          listToStr = ' '.join([str(elem) for elem in content])
          Texto = listToStr.replace('\n','').replace('  ','').replace('_','').split(".", 3)[3]

    Texto_list.append(Texto)

  except:
    Texto_list.append(' ')


# # Criando o banco de Dados Brutos

# In[47]:


import pandas as pd

# Criando um DataFrame para alocar os outputs

dados = pd.DataFrame (ID ,columns=['ID'])
dados['Texto_lei'] = Texto_list
dados['Data_lei'] = Data_lei
dados['Data_publicação'] = ['']*len(Texto_list)
dados['Revogada'] = lista_revogada
dados['Tipo_lei'] = tipo
dados['Setor'] = ['Anac']*len(Texto_list)

dados


# In[49]:


# Exportando o banco de dados

dados.to_csv("Resolucao_anac.txt", index=False, encoding='utf-8-sig', sep = '汉')


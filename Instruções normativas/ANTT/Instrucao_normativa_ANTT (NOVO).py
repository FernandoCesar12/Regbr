#!/usr/bin/env python
# coding: utf-8

# # ATOS NORMATIVOS

# ### Pegando os links de acesso á página (2021)

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

import pandas as pd
import time
import re

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = "https://anttlegis.antt.gov.br/action/ActionDatalegis.php?acao=abrirResenhaAnoAto&cod_modulo=161&cod_menu=7797&ano=2021"
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)

soup = BeautifulSoup(driver.page_source, 'lxml')
posicao = soup.find_all("div", {"class": "ementa"})
    
    
link_lista = []
for i in range(0,len(posicao)):
    if 'href="/' in str(posicao[i]):
        result = str(posicao[i]).split('href="/',1)[1].split('" target=')[0].replace('amp;','')
        link_lista.append(result)
    
append_str = 'https://anttlegis.antt.gov.br/'
Link_2021 = [append_str + sub for sub in link_lista]    


# ### Pegando os links de acesso á página (2020)

# In[3]:


#pip install selenium

#!apt install chromium-chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import time
import re

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = "https://anttlegis.antt.gov.br/action/ActionDatalegis.php?acao=abrirResenhaAnoAto&cod_modulo=161&cod_menu=7797&ano=2020"
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)

soup = BeautifulSoup(driver.page_source, 'lxml')
posicao = soup.find_all("div", {"class": "ementa"})
    
    
link_lista = []
for i in range(0,len(posicao)):
    if 'href="/' in str(posicao[i]):
        result = str(posicao[i]).split('href="/',1)[1].split('" target=')[0].replace('amp;','')
        link_lista.append(result)
    
append_str = 'https://anttlegis.antt.gov.br/'
Link_2020 = [append_str + sub for sub in link_lista]    


# ### Pegando os conteudos dentro dos links

# In[6]:


#pip install selenium

#!apt install chromium-chromedriver

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import time
import re

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url = Link_2021+Link_2020

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

Texto_revogados = []

for i in range(0,len(url)):
    
    driver.get(url[i])
    driver.implicitly_wait(30)
    
    time.sleep(10)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    posicao = soup.find_all("div", {"id": "conteudo"})
    
    Texto_revogados.append(posicao)


# ### Separando as variáveis

# In[34]:


# Separando número e ano da resolução

info = []
    
for i in range(0,len(Texto_revogados)):
    result = re.findall(r'\d+\/\d+', str(Texto_revogados[i]))[0]
    info.append(result)

num = []
for i in range(0,len(info)):
    result = info[i].split('/')[0]
    num.append(result)
    
ano = []
for i in range(0,len(info)):
    result = info[i].split('/')[1]
    ano.append(result)
    
Tipo = ['806']*len(Texto_revogados) # Tipo de Lei

parte1 = [i + j for i, j in zip(Tipo, num)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano)] 

   
# Separando a data da resolução

data_resolucao = []
    
for i in range(0,len(Texto_revogados)):
    try:
        result = re.findall(r'\d+ DE [JANEIRO]*[FEVEREIRO]*[MARÇO]*[ABRIL]*[MAIO]*[JUNHO]*[JULHO]*[AGOSTO]*[SETEMBRO]*[OUTUBRO]*[NOVEMBRO]*[DEZEMBRO]* DE \d+', str(Texto_revogados[i]))[0]
        data_resolucao.append(result)
    except:
        data_resolucao.append('')
    
# Fazendo uma limpeza no texto

import re

texto_limpo = []

for i in range(0,len(Texto_revogados)):
    texto_limpo.append(re.sub('<[^>]+>', '', str(Texto_revogados[i])).replace('\n','').replace('\t','').replace('\xa0 ',''))
        
    
# Revogados

Resultado_revoga = []
for i in range(0,len(Texto_revogados)):
    if 'REVOGADA' in str(Texto_revogados[i]).upper():
        result = True
        Resultado_revoga.append(result)
    else:
        result = False
        Resultado_revoga.append(result)

# Criando um DataFrame para alocar os outputs

BANCO = pd.DataFrame (ID ,columns=['ID'])
BANCO['Texto_lei'] = texto_limpo
BANCO['Data_lei'] = data_resolucao
BANCO['Data_publicação'] = ['']*len(texto_limpo)
BANCO['Tipo_lei'] = Tipo
BANCO['Revogada'] = Revogados
BANCO['Setor'] = ['ANM']*len(texto_limpo)

BANCO


# ### Exportando os dados

# In[35]:


# Exportando em formato TXT

BANCO.to_csv("Instrucao_Normativa_ANTT.txt", index=False, encoding='utf-8-sig', sep = '汉')


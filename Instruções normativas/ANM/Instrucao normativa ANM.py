#!/usr/bin/env python
# coding: utf-8

# ## ATOS NORMATIVOS REVOGADOS

# ### Pegando os links de acesso á página

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

url = "https://anmlegis.datalegis.inf.br/action/ActionDatalegis.php?acao=recuperarTematicasCollapse&cod_modulo=414&cod_menu=7903&letra=INSTRU%C7%D5ES%20NORMATIVAS%20(14)&co_tematica=14024375"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)

soup = BeautifulSoup(driver.page_source, 'lxml')
posicao = soup.find_all("div", {"class": "ementa"})
    
    
link_lista = []
for i in range(0,len(posicao)):
    if 'href="/' in str(posicao[i]):
        result = str(posicao[i]).split('href="/',1)[1].split('" property="url"',1)[0].replace('amp;','')
        link_lista.append(result)
    
append_str = 'https://anmlegis.datalegis.inf.br/'
Link = [append_str + sub for sub in link_lista]    


# ### Pegando os conteudos dentro dos links

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

url = Link

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

# In[67]:


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
    
Tipo = ['706']*len(Texto_revogados) # Tipo de Lei

parte1 = [i + j for i, j in zip(Tipo, num)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano)] 

# Separando a data de publicação no DOU

data_dou = []
for i in range(0,len(Texto_revogados)):
    if 'D.O.U.,' in str(Texto_revogados[i]):
        result = str(Texto_revogados[i]).split('D.O.U.,')[1].split('-')[0].split('</p>')[0].replace('<br/>REP., 26/02/2001','')
        data_dou.append(result)
    else:
        data_dou.append('')
    
    
# Separando a data da resolução

data_resolucao = []
    
for i in range(0,len(Texto_revogados)):
    try:
        result = re.findall(r'\d+ DE [JANEIRO]*[FEVEREIRO]*[MARÇO]*[ABRIL]*[MAIO]*[JUNHO]*[JULHO]*[AGOSTO]*[SETEMBRO]*[OUTUBRO]*[NOVEMBRO]*[DEZEMBRO]* DE \d+', str(Texto_revogados[i]))[0]
        data_resolucao.append(result)
    except:
        data_resolucao.append('')
    
# Fazendo uma limpeza no texto

texto_limpo = []
for i in range(0,len(Texto_revogados)):

    result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('\xa0',' ').replace('<p style="text-align: center;">','').split('<div class="ato" property="articleBody">')[1]
    texto_limpo.append(result)
    
# Revogados

Revogados  = [True]*len(Texto_revogados)

# Criando um DataFrame para alocar os outputs

BANCO_REVOGADOS = pd.DataFrame (ID ,columns=['ID'])
BANCO_REVOGADOS['Texto_lei'] = texto_limpo
BANCO_REVOGADOS['Data_lei'] = data_resolucao
BANCO_REVOGADOS['Data_publicação'] = data_dou
BANCO_REVOGADOS['Tipo_lei'] = Tipo
BANCO_REVOGADOS['Revogada'] = Revogados
BANCO_REVOGADOS['Setor'] = ['ANM']*len(texto_limpo)

BANCO_REVOGADOS


# ## ATOS NORMATIVOS VIGENTES

# ### Pegando os links de acesso á página

# In[69]:


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

url = "https://anmlegis.datalegis.inf.br/action/ActionDatalegis.php?acao=recuperarTematicasCollapse&cod_menu=7351&cod_modulo=414"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)

soup = BeautifulSoup(driver.page_source, 'lxml')
posicao = soup.find_all("div", {"class": "ementa"})
    
    
link_lista = []
for i in range(0,len(posicao)):
    if 'href="/' in str(posicao[i]):
        result = str(posicao[i]).split('href="/',1)[1].split('" property="url"',1)[0].replace('amp;','')
        link_lista.append(result)
    
append_str = 'https://anmlegis.datalegis.inf.br/'
Link = [append_str + sub for sub in link_lista]    


# ### Pegando os conteudos dentro dos links

# In[70]:


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

url = Link

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

# In[71]:


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
    
Tipo = ['706']*len(Texto_revogados) # Tipo de Lei

parte1 = [i + j for i, j in zip(Tipo, num)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano)] 

# Separando a data de publicação no DOU

data_dou = []
for i in range(0,len(Texto_revogados)):
    if 'D.O.U.,' in str(Texto_revogados[i]):
        result = str(Texto_revogados[i]).split('D.O.U.,')[1].split('-')[0].split('</p>')[0].replace('<br/>REP., 26/02/2001','')
        data_dou.append(result)
    else:
        data_dou.append('')
    
    
# Separando a data da resolução

data_resolucao = []
    
for i in range(0,len(Texto_revogados)):
    try:
        result = re.findall(r'\d+ DE [JANEIRO]*[FEVEREIRO]*[MARÇO]*[ABRIL]*[MAIO]*[JUNHO]*[JULHO]*[AGOSTO]*[SETEMBRO]*[OUTUBRO]*[NOVEMBRO]*[DEZEMBRO]* DE \d+', str(Texto_revogados[i]))[0]
        data_resolucao.append(result)
    except:
        data_resolucao.append('')
    
# Fazendo uma limpeza no texto

texto_limpo = []
for i in range(0,len(Texto_revogados)):

    result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('\xa0',' ').replace('<p style="text-align: center;">','').split('<div class="ato" property="articleBody">')[1]
    texto_limpo.append(result)
    
# Revogados

Revogados  = [True]*len(Texto_revogados)

# Criando um DataFrame para alocar os outputs

BANCO_VIGENTES = pd.DataFrame (ID ,columns=['ID'])
BANCO_VIGENTES['Texto_lei'] = texto_limpo
BANCO_VIGENTES['Data_lei'] = data_resolucao
BANCO_VIGENTES['Data_publicação'] = data_dou
BANCO_VIGENTES['Tipo_lei'] = Tipo
BANCO_VIGENTES['Revogada'] = Revogados
BANCO_VIGENTES['Setor'] = ['ANM']*len(texto_limpo)

BANCO_VIGENTES


# ### Exportando os dados

# In[72]:


# Concatenando os bancos de dados

BANCO = BANCO_REVOGADOS.append(BANCO_VIGENTES)
BANCO = BANCO.reset_index()
del BANCO['index']

# Exportando em formato TXT

BANCO.to_csv("Instrucao_normativa_ANM.txt", index=False, encoding='utf-8-sig', sep = '汉')


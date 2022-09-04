#!/usr/bin/env python
# coding: utf-8

# # ATOS NORMATIVOS REVOGADOS

# ## Pegando os links de acesso á página

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

url = "https://anmlegis.datalegis.inf.br/action/ActionDatalegis.php?acao=recuperarTematicasCollapse&cod_modulo=414&cod_menu=7903&letra=PORTARIAS%20(132)&co_tematica=14024372"

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


# ## Pegando os conteudos dentro dos links

# In[2]:


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


# ## Separando as variáveis

# In[3]:


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

# Separando a data de publicação no DOU

data_dou = []
for i in range(0,len(Texto_revogados)):
    result = str(Texto_revogados[i]).rsplit('D.O.U.')[-1].split('-')[0].replace('</p> <p style="font','').replace('Seção 1','').replace(',','').replace(' ','').replace('</p><p>\tRET.19/09/2003</p><p>\t\xa0','').replace('</p><p>REP.28/07/2005','')
    data_dou.append(result)
    
    
# Separando a data da resolução

data_resolucao_1 = []
    
for i in range(0,len(Texto_revogados)):
    data_resolucao_1.append(str(Texto_revogados[i]).split('PORTARIA N')[1].split('</p>')[0].replace('\xa0',''))
    
data_resolucao_2 = []

for i in range(0,len(data_resolucao_1)):
    if ',' in str(data_resolucao_1[i]):
        result = str(data_resolucao_1[i]).split(',')[1].split(' ',2)[2]
        data_resolucao_2.append(result)
    else:
        result = str(data_resolucao_1[i])
        data_resolucao_2.append(result)
        
        
data_resolucao = []

for i in range(0,len(data_resolucao_2)):
    if '<br/>' in str(data_resolucao_2[i]):
        result = str(data_resolucao_2[i]).split('<br/>')[0]
        data_resolucao.append(result)
    else:
        data_resolucao.append(data_resolucao_2[i])
    
# Fazendo uma limpeza no texto


texto_limpo = []
for i in range(0,len(Texto_revogados)):
    if 'MINISTÉRIO DE MINAS E ENERGIA' in str(Texto_revogados[i]):
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('MINISTÉRIO DE MINAS E ENERGIA')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    elif 'MINISTÉRIO DE MINAS ENERGIA' in str(Texto_revogados[i]):
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('MINISTÉRIO DE MINAS ENERGIA')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    elif 'DEPARTAMENTO NACIONAL DE PRODUÇÃO MINERAL' in str(Texto_revogados[i]):
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('DEPARTAMENTO NACIONAL DE PRODUÇÃO MINERAL')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    else: 
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').replace('<p style="margin-left: 50%; text-align: justify;">','')
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


# # ATOS NORMATIVOS VIGENTES

# ## Pegando os links de acesso á página

# In[4]:


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

url = "https://anmlegis.datalegis.inf.br/action/ActionDatalegis.php?acao=recuperarTematicasCollapse&cod_menu=7349&cod_modulo=414"

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


# ## Pegando os conteudos dentro dos links

# In[5]:


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


# ## Separando as variáveis

# In[6]:


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

# Separando a data de publicação no DOU

data_dou_1 = []
for i in range(0,len(Texto_revogados)):
    result = str(Texto_revogados[i]).rsplit('D.O.U.')[-1].split('-')[0].replace('</p> <p style="font','').replace('Seção 1','').replace(',','').replace(' ','').replace('<ahref="javascript:LinkTexto(\'POR\'\'00000311\'\'RET\'\'2005\'\'DNPM/MME\'\'\'\'\'\'\')"></a></p><p><ahref="javascript:LinkTexto(\'POR\'\'00000311\'\'RET\'\'2005\'\'DNPM/MME\'\'\'\'\'\'\')">RET.16/12/2005</a>','').replace('</p><p>RET.18/02/2004','').replace('</p><br/><pstyle="text','')
    data_dou_1.append(result)
    
data_dou = [] 
for i in range(0,len(data_dou_1)):
    if len(data_dou_1[i]) >= 20:
        data_dou.append(' ')
    else:
        data_dou.append(data_dou_1[i])
    
    
# Separando a data da resolução

data_resolucao_1 = []

for i in range(0,len(Texto_revogados)):
    data_resolucao_1.append(str(Texto_revogados[i]).split('PORTARIA')[1].split('</p>')[0].replace('\xa0',''))
    
data_resolucao_2 = []

for i in range(0,len(data_resolucao_1)):
    if ',' in str(data_resolucao_1[i]):
        result = str(data_resolucao_1[i]).split(',')[1].split(' ',2)[2]
        data_resolucao_2.append(result)
    else:
        result = str(data_resolucao_1[i])
        data_resolucao_2.append(result)
        
        
data_resolucao = []

for i in range(0,len(data_resolucao_2)):
    if '<br/>' in str(data_resolucao_2[i]):
        result = str(data_resolucao_2[i]).split('<br/>')[0]
        data_resolucao.append(result)
    else:
        data_resolucao.append(data_resolucao_2[i])
    
# Fazendo uma limpeza no texto


texto_limpo = []
for i in range(0,len(Texto_revogados)):
    if 'MINISTÉRIO DE MINAS E ENERGIA' in str(Texto_revogados[i]):
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('MINISTÉRIO DE MINAS E ENERGIA')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    elif 'MINISTÉRIO DE MINAS ENERGIA' in str(Texto_revogados[i]):
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('MINISTÉRIO DE MINAS ENERGIA')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    elif 'DEPARTAMENTO NACIONAL DE PRODUÇÃO MINERAL' in str(Texto_revogados[i]):
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').split('DEPARTAMENTO NACIONAL DE PRODUÇÃO MINERAL')[1].replace('<p style="margin-left: 50%; text-align: justify;">','')
        texto_limpo.append(result)
        
    else: 
        
        result = str(Texto_revogados[i][0]).replace('</p>','').replace('\t','').replace('\n','').replace('<p>','').replace('</div>','').replace('<br/>','').replace('<p style="text-align: center;">','').replace('<p style="margin-left: 50%; text-align: justify;">','')
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


# # Exportando os dados

# In[7]:


# Concatenando os bancos de dados

BANCO = BANCO_REVOGADOS.append(BANCO_VIGENTES)
BANCO = BANCO.reset_index()
del BANCO['index']

# Exportando em formato TXT

BANCO.to_csv("Portarias_ANM.txt", index=False, encoding='utf-8-sig', sep = '汉')


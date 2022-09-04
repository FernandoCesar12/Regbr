#!/usr/bin/env python
# coding: utf-8

# # Realizando a extração dos links das portarias

# ### Vigentes

# In[8]:


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

    
url = "https://www.gov.br/ana/pt-br/acesso-a-informacao/legislacao/atos-normativos/pesquisa-atos-normativos"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

# Pega o XPath do iframe e atribui a uma variável
iframe = driver.find_element_by_xpath('//*[@id="ifrResolucoes"]')

# Muda o foco para o iframe
driver.switch_to.frame(iframe)

Ano = ['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007',
       '2006','2005','2004','2003','2002','2001']

links_ano = []
titulo = []

for i in range(0,len(Ano)):

    # Seleciona o Ano

    select1 = Select(driver.find_element_by_id('cmbAno'))
    select1.select_by_value(Ano[i])
    time.sleep(5)

    
    # Seleciona as portarias 

    select1 = Select(driver.find_element_by_id('cmbTipoAto'))
    select1.select_by_value('Resolução')
    time.sleep(5)


    # Realizando a extração das informações no site

    soup_link = BeautifulSoup(driver.page_source, 'lxml')

    href = ' '.join([str(elem) for elem in soup_link]).split('onclick')

    links = []
    for i in range(0,len(href)):
        if 'abreArquivo' in str(href[i]) and '<b>' in str(href[i]):
            result = href[i].split("abreArquivo(\'")[1].split("')")[0]
            links.append(result)
    
    # Removendo duplicadas

    links_portarias = list(set(links))

    links_ano.append(links_portarias)
    
    # Pegando as informações de titulo
    
    nome_portaria = soup_link.find_all('div', class_='titulo_resolucao')

    for i in range(0,len(nome_portaria)):
        if 'Resolução' in str(nome_portaria[i]):
            titulo.append(str(nome_portaria[i]).split('<b>')[1].split('</b>')[0])
   
# Separando os links finais 

flat_list_vigente = [item for sublist in links_ano for item in sublist]

# Criando o ID

tipo = ['701']*len(titulo) # Tipo de Lei

Num = []

for i in range(0,len(titulo)):
    try:
        if ',' in str(titulo[i]) and 'nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('nº')[1].split(',')[0].replace(' ','')) # Número da portaria
            
        elif ',' in str(titulo[i]) and 'Nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('Nº')[1].split(',')[0].replace(' ','')) # Número da portaria
            
        elif ',' not in str(titulo[i]) and 'Nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('Nº')[1].split('de')[0].replace(' ','')) # Número da portaria
            
        elif ',' not in str(titulo[i]) and 'nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('nº')[1].split('de')[0].replace(' ','')) # Número da portaria
    except:
        Num.append('00')
    
Ano = []

for i in range(0,len(titulo)): # Pegando o ano da portaria
    try:
        Ano.append(titulo[i][-4:])
    except:
        Ano.append('0000')
    
parte1 = [i + j for i, j in zip(tipo, Num)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano)] 


# Data da Portaria

Data_portaria = []
for i in range(0,len(titulo)):
    try:
        result = str(titulo[i]).split(', de')[1]
        Data_portaria.append(result)
    except:
        Data_portaria.append(' ')
        
# Revogação 

Revogado = [True]*len(ID)


# In[10]:


import pandas as pd

# Criando um DataFrame para alocar os outputs

BANCO_vigente = pd.DataFrame (ID ,columns=['ID'])
BANCO_vigente['Link'] = flat_list_vigente
BANCO_vigente['Data_lei'] = ['']*len(flat_list_vigente)
BANCO_vigente['Data_publicação'] = Data_portaria
BANCO_vigente['Tipo_lei'] = tipo
BANCO_vigente['Setor'] = ['ANA']*len(ID)
BANCO_vigente['Revogada'] = Revogado

BANCO_vigente


# ### Revogados

# In[18]:


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

    
url = "https://www.gov.br/ana/pt-br/acesso-a-informacao/legislacao/atos-normativos/pesquisa-atos-normativos"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

# Pega o XPath do iframe e atribui a uma variável
iframe = driver.find_element_by_xpath('//*[@id="ifrResolucoes"]')

# Muda o foco para o iframe
driver.switch_to.frame(iframe)

Ano = ['2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007',
       '2006','2005','2004','2003','2002','2001']

links_ano = []
titulo = []

for i in range(0,len(Ano)):

    # Seleciona o Ano

    select1 = Select(driver.find_element_by_id('cmbAno'))
    select1.select_by_value(Ano[i])
    time.sleep(5)
    
    # Seleciona os revogados e vingentes 
    
    # driver.find_element_by_xpath('//*[@id="rdVisualizacaoCompleta"]').click();
    driver.find_element_by_xpath('//*[@id="rdVisualizacaoRevogadas"]').click();
    time.sleep(5)
    
    # Seleciona as portarias 

    select1 = Select(driver.find_element_by_id('cmbTipoAto'))
    select1.select_by_value('Resolução')
    time.sleep(5)


    # Realizando a extração das informações no site

    soup_link = BeautifulSoup(driver.page_source, 'lxml')

    href = ' '.join([str(elem) for elem in soup_link]).split('onclick')

    links = []
    for i in range(0,len(href)):
        if 'abreArquivo' in str(href[i]) and '<b>' in str(href[i]):
            result = href[i].split("abreArquivo(\'")[1].split("')")[0]
            links.append(result)
    
    # Removendo duplicadas

    links_portarias = list(set(links))

    links_ano.append(links_portarias)
    
    # Pegando as informações de titulo
    
    nome_portaria = soup_link.find_all('div', class_='titulo_resolucao')

    for i in range(0,len(nome_portaria)):
        if 'Resolução' in str(nome_portaria[i]):
            titulo.append(str(nome_portaria[i]).split('<b>')[1].split('</b>')[0])
   
# Separando os links finais 

flat_list_vigente = [item for sublist in links_ano for item in sublist]

# Criando o ID

tipo = ['701']*len(titulo) # Tipo de Lei

Num = []

for i in range(0,len(titulo)):
    try:
        if ',' in str(titulo[i]) and 'nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('nº')[1].split(',')[0].replace(' ','')) # Número da portaria
            
        elif ',' in str(titulo[i]) and 'Nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('Nº')[1].split(',')[0].replace(' ','')) # Número da portaria
            
        elif ',' not in str(titulo[i]) and 'Nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('Nº')[1].split('de')[0].replace(' ','')) # Número da portaria
            
        elif ',' not in str(titulo[i]) and 'nº' in str(titulo[i]):
            Num.append(str(titulo[i]).split('nº')[1].split('de')[0].replace(' ','')) # Número da portaria
    except:
        Num.append('00')
    
Ano = []

for i in range(0,len(titulo)): # Pegando o ano da portaria
    try:
        Ano.append(titulo[i][-4:])
    except:
        Ano.append('0000')
    
parte1 = [i + j for i, j in zip(tipo, Num)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano)] 


# Data da Portaria

Data_portaria = []
for i in range(0,len(titulo)):
    try:
        result = str(titulo[i]).split(', de')[1]
        Data_portaria.append(result)
    except:
        Data_portaria.append(' ')
        
# Revogação 

Revogado = [False]*len(ID)


# In[19]:


import pandas as pd

# Criando um DataFrame para alocar os outputs

BANCO_revogado = pd.DataFrame (ID ,columns=['ID'])
BANCO_revogado['Link'] = flat_list_vigente
BANCO_revogado['Data_lei'] = ['']*len(flat_list_vigente)
BANCO_revogado['Data_publicação'] = Data_portaria
BANCO_revogado['Tipo_lei'] = tipo
BANCO_revogado['Setor'] = ['ANA']*len(ID)
BANCO_revogado['Revogada'] = Revogado

BANCO_revogado


# ### Juntando os Dataframes

# In[22]:


BANCO = pd.concat([BANCO_vigente,BANCO_revogado])

# Exportando em formato TXT

BANCO.to_csv("Resolucao_ANA_link.txt", index=False, encoding='utf-8-sig', sep = '汉')


# In[23]:


BANCO


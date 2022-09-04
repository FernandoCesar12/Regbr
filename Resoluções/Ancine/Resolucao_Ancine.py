#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das resoluções

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

url = "https://www.gov.br/ancine/pt-br/acesso-a-informacao/legislacao/resolucoes-diretoria-colegiada"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)
        
soup = BeautifulSoup(driver.page_source, 'lxml')

texto = ' '.join([str(elem) for elem in soup]).split('data-tippreview-image=""')

conteudo_textual = []

for i in range(0,len(texto)):
    if 'target="_self">' in str(texto[i]):
        result = str(texto[i]).split('target="_self">')[0].rsplit('href="')[1].replace(' ','').replace('"','')
        conteudo_textual.append(result)
        
links = list(dict.fromkeys(conteudo_textual))

links_limpeza = []
for i in range(0,len(links)):
    if 'target=' in str(links[i]):
        links_limpeza.append(str(links[i]).split('target=')[0])
    else:
        links_limpeza.append(str(links[i]))


# # Pegando o conteudo textual dos links HTML

# In[50]:


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

for i in range(0,len(links_limpeza)):
    if '.pdf' not in str(links_limpeza[i]) and '.doc' not in str(links_limpeza[i]) and '.xlsx' not in str(links_limpeza[i]):
        link_html.append(links_limpeza[i])
        
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


# ### Separando o conteúdo em variáveis

# In[51]:


# Separando as datas das resoluções
                  
Ano_lei = []
for i in range(0,len(Titulo)):

    result = str(Titulo[i]).replace(' ','').replace('.','')[-4:]
    Ano_lei.append(result)
    
Ano_lei_2 = []
for i in range(0,len(Ano_lei)):

    result = str(Ano_lei[i]).replace('ste…','0000')
    Ano_lei_2.append(result)  
    
Num_lei = []

for i in range(0,len(Titulo)):
    
    if 'n.º' in str(Titulo[i]):

        result = str(Titulo[i]).split('n.º')[1].split(',')[0].replace(' ','').replace(',','')
        Num_lei.append(result)
        
    else:
        
        result = str('000')
        Num_lei.append(result)
        

# Criando o ID

Tipo = ['710']*len(Titulo) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei_2)] 

# Separando a data de publicação no DOU
    
Data_lei = []

for i in range(0,len(Titulo)):
    
    if ', de' in str(Titulo[i]):

        result = str(Titulo[i]).split(', de')[1]
        Data_lei.append(result)
        
    else:
        
        result = ' '
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


# ### Visualizando as variáveis do Banco de Dados Brutos

# In[52]:


import pandas as pd
import numpy as np

# Criando um DataFrame para alocar os outputs

BANCO_HTML = pd.DataFrame (ID ,columns=['ID'])
BANCO_HTML['Texto_lei'] = Titulo
BANCO_HTML['Data_lei'] = Data_lei
BANCO_HTML['Data_publicação'] = Data_lei
BANCO_HTML['Tipo_lei'] = Tipo
BANCO_HTML['Revogada'] = Revogada
BANCO_HTML['Setor'] = ['ANCINE']*len(Titulo)

BANCO_HTML


# # Pegando o conteudo textual dos PDFS

# In[63]:


# Separando os links que estão em pdf

link_PDF = []


for i in range(0,len(links)):
    if '.pdf' in str(links[i]):
        link_PDF.append(str(links[i]).split('.pdf')[0]+'.pdf')
        

# Entrando com os pacotes necessários

import re
import io
import requests
from PyPDF2 import PdfFileReader


#Selecionando a URL

url_list = link_PDF

Texto_pdf = []

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
        Texto_pdf.append(listToStr)
        
    except:
        Texto_pdf.append('')
        
Texto_filtro = []
for i in range(0,len(Texto_pdf)):
    if len(str(Texto_pdf[i])) > 200 and 'RESOLUÇÃO' in str(Texto_pdf[i]).upper() and 'Nº' in str(Texto_pdf[i]).upper():
        Texto_filtro.append(str(Texto_pdf[i]))


# ### Separando o conteúdo em variáveis

# In[95]:


Num_lei = []
for i in range(0,len(Texto_filtro)):
    result = str(Texto_filtro[i]).split('Nº')[1].split(' ',2)[1]
    Num_lei.append(result)
    
Ano_lei = []
for i in range(0,len(Texto_filtro)):
    result = str(Texto_filtro[i]).split('Decreto nº')[1].split(',',2)[1][-4:]
    Ano_lei.append(result)
    
# Criando o ID

Tipo = ['710']*len(Texto_filtro) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei)] 

Data_lei = []
for i in range(0,len(Texto_filtro)):
    result = str(Texto_filtro[i]).split('Decreto nº')[1].split(',',2)[1]
    Data_lei.append(result)
    
# Separando se a resolução foi revogada
    
Revogada = []

for i in range(0,len(Texto_filtro)):
    if 'Revogada' in Texto_filtro[i] or 'REVOGADA' in Texto_filtro[i] or 'revogada' in Texto_filtro[i]:
        result = True
        Revogada.append(result)
    
    else:
        result = False
        Revogada.append(result)


# ### Visualizando as variáveis do Banco de Dados Brutos

# In[96]:


import pandas as pd
import numpy as np

# Criando um DataFrame para alocar os outputs

BANCO_PDF = pd.DataFrame (ID ,columns=['ID'])
BANCO_PDF['Texto_lei'] = Texto_filtro
BANCO_PDF['Data_lei'] = Data_lei
BANCO_PDF['Data_publicação'] = Data_lei
BANCO_PDF['Tipo_lei'] = Tipo
BANCO_PDF['Revogada'] = Revogada
BANCO_PDF['Setor'] = ['ANCINE']*len(Texto_filtro)

BANCO_PDF


# # Exportando a base de dados

# In[97]:


import pandas as pd 

BANCO = pd.concat([BANCO_HTML,BANCO_PDF])
BANCO.to_csv("Resolucao.txt", index=False, encoding='utf-8-sig', sep = '汉')


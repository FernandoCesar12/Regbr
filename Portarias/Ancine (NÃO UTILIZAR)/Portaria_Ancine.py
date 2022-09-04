#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das portarias

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

url = "https://www.gov.br/ancine/pt-br/acesso-a-informacao/legislacao/portarias"

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
    if '.pdf' not in str(links[i]) and '.doc' not in str(links[i]) and '.xlsx' not in str(links[i]):
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
            
        if 'rgb(' in str(soup):
            titulo_html.append(re.sub('<[^>]+>', '', str(soup).split('rgb(')[1].split('</a>')[0].replace('\n','').replace('  ','')))
            texto_html.append(re.sub('<[^>]+>', '', str(soup).replace('\n','')))
            
        elif 'color="#000080" face="Arial">' in str(soup):
            titulo_html.append(re.sub('<[^>]+>', '', str(soup).split('color="#000080" face="Arial">')[1].split('</a>')[0].replace('\n','').replace('  ','').replace(' face="Arial">','')))
            texto_html.append(re.sub('<[^>]+>', '', str(soup).replace('\n','')))
                
        else:
            titulo_html.append('')
            texto_html.append('')    
            
Titulo_html = []
for i in range(0,len(titulo_html)):
    if '0,0,128)">' in str(titulo_html[i]):
        Titulo_html.append(str(titulo_html[i]).split('0,0,128)">')[1])
    else: 
        Titulo_html.append(str(titulo_html[i]))


# ### Separando o conteúdo em variáveis

# In[20]:


# Separando as datas das resoluções
                  
Ano_lei = []
for i in range(0,len(Titulo_html)):
    
    try:

        result = str(Titulo_html[i]).replace(' ','').replace('.','')[-4:]
        Ano_lei.append(result)
        
    except:
        Ano_lei.append('0000')
        
        
Ano_lei_2 = []

for i in range(0,len(Ano_lei)):
    if len(str(Ano_lei[i])) <1:
        Ano_lei_2.append('0000')
    else:
        Ano_lei_2.append(str(Ano_lei[i]))
        
    
Num_lei = []

for i in range(0,len(Titulo_html)):
    
    try:
    
        if 'LEI' not in str(Titulo_html[i]).upper():

            result = str(Titulo_html[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').split('Nº')[1].split(' ',2)[1].replace(' ','').replace(',','').replace('.','').replace('-','').replace('E','')
            Num_lei.append(result)
        
        else:
        
            result = str(Titulo_html[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').replace('NO','Nº').split('Nº')[1].split(' ',2)[1].replace(' ','').replace(',','').replace('.','').replace('-','').replace('E','')
            Num_lei.append(result)
            
    except: 
        
        Num_lei.append('0000')
        
Num_lei_2 = []

for i in range(0,len(Num_lei)):
    if len(str(Num_lei[i])) <1:
        Num_lei_2.append('000')
    else:
        Num_lei_2.append(str(Num_lei[i]))
        
# Criando o ID

Tipo = ['710']*len(Titulo_html) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei_2)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei_2)] 

# Separando a data de publicação no DOU
    
Data_lei = []

for i in range(0,len(Titulo_html)):
    
    try:
    
        if 'LEI' not in str(Titulo_html[i]).upper():

            result = str(Titulo_html[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').split('Nº')[1].split(' ',3)[3].replace(',','').replace('.','').replace('-','')
            Data_lei.append(result)
        
        else:
        
            result = str(Titulo_html[i]).upper().replace('n.º','Nº').replace('No','Nº').replace('N.º','Nº').replace('NO','Nº').split('Nº')[1].split(' ',3)[3].replace(',','').replace('.','').replace('-','')
            Data_lei.append(result)
            
    except:
        
        Data_lei.append(' ')
        
# Separando se a resolução foi revogada
    
Revogada = []

for i in range(0,len(Titulo_html)):
    if 'Revogada' in Titulo_html[i] or 'REVOGADA' in Titulo_html[i] or 'revogada' in Titulo_html[i]:
        result = True
        Revogada.append(result)
    
    else:
        result = False
        Revogada.append(result)


# ### Visualizando as variáveis do Banco de Dados Brutos

# In[21]:


import pandas as pd
import numpy as np

# Criando um DataFrame para alocar os outputs

BANCO_HTML = pd.DataFrame (ID ,columns=['ID'])
BANCO_HTML['Texto_lei'] = Titulo_html
BANCO_HTML['Data_lei'] = Data_lei
BANCO_HTML['Data_publicação'] = Data_lei
BANCO_HTML['Tipo_lei'] = Tipo
BANCO_HTML['Revogada'] = Revogada
BANCO_HTML['Setor'] = ['ANCINE']*len(Titulo_html)

BANCO_HTML


#    # Pegando o conteudo textual dos PDFs

# In[22]:


# Separando os links que estão em pdf

link_PDF = []

for i in range(0,len(links)):
    if '.pdf' in str(links[i]):
        link_PDF.append(links[i])
        
for i in range(0,len(link_html)):
    if '" style="' in str(link_html[i]):
        link_PDF[i] = str(link_html[i]).split('" style="')[0]

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
    if len(str(Texto_pdf[i])) > 200 and 'PORTARIA' in str(Texto_pdf[i]).upper() and 'Nº' in str(Texto_pdf[i]).upper():
        Texto_filtro.append(str(Texto_pdf[i]))


# ### Separando o conteúdo em variáveis

# In[26]:


# Separando as datas das resoluções
                  
Ano_lei = []
for i in range(0,len(Texto_filtro)):
    
    if 'ISSN' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('ISSN')[0][-7:].replace(' ','').replace('e','')[0:4].replace('.','')
        Ano_lei.append(result)
        
    elif 'Torna' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Torna')[0][-7:].replace(' ','').replace('E','').replace('.','')
        Ano_lei.append(result)
        
    elif 'A DIRETORA' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('A DIRETORA')[0][-7:].replace(' ','').replace('.','')
        Ano_lei.append(result)
        
    elif 'O DIRETOR' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]) and 'Torna' not in str(Texto_filtro[i]) and 'Dispõe' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('O DIRETOR')[0].replace(' ','')[-5:].replace('e','').replace('E','').replace('.','')
        Ano_lei.append(result)
        
    elif 'Dispõe' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Dispõe')[0][-8:].replace(' ','').replace('e','')[0:4].replace('.','')
        Ano_lei.append(result)
    
    elif 'Em atendimento' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Em atendimento')[0].replace(' ','').replace('.','')[-4:]
        Ano_lei.append(result)
        
    else:
        Ano_lei.append('0000')
    
Num_lei = []
for i in range(0,len(Texto_filtro)):
    
    if 'ISSN' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('ISSN')[0].replace('N.º','Nº').split('Nº')[1].split(',')[0].replace(' ','')
        Num_lei.append(result)
        
    elif 'Torna' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Torna')[0].replace('N.º','Nº').split('Nº')[1].split(',')[0].replace(' ','')
        Num_lei.append(result)
        
    elif 'A DIRETORA' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('A DIRETORA')[0].replace('N.º','Nº').split('Nº')[1].split(',')[0].replace(' ','')
        Num_lei.append(result)
        
    elif 'O DIRETOR' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]) and 'Torna' not in str(Texto_filtro[i]) and 'Dispõe' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('O DIRETOR')[0].replace('N.º','Nº').replace('N°','Nº').split('Nº')[1].split(',')[0].replace(' ','').replace('de04deJANEIROde2016','').replace(' ','')
        Num_lei.append(result)
        
    elif 'Dispõe' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Dispõe')[0].replace('N.º','Nº').replace('N°','Nº').split('Nº')[1].split(',')[0].replace(' ','').replace(' ','')
        Num_lei.append(result)
    
    elif 'Em atendimento' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Em atendimento')[0].replace(' ','').replace('.','').replace('nº','Nº').replace('de','DE').split('Nº')[1].split('DE')[0].replace(',','').replace(' ','')
        Num_lei.append(result)
        
    else: 
        Num_lei.append('000')
        
# Criando o ID

Tipo = ['710']*len(Texto_filtro) # Tipo de Lei
                            
parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei)] 

# Separando a data de publicação no DOU
    
Data_lei = []
for i in range(0,len(Texto_filtro)):
    
    if 'ISSN' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('ISSN')[0].replace('N.º','Nº').split('Nº')[1].split(',',1)[1][:-1]
        Data_lei.append(result)
        
    elif 'Torna' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Torna')[0].replace('N.º','Nº').split('Nº')[1].split(',')[1]
        Data_lei.append(result)
        
    elif 'A DIRETORA' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('A DIRETORA')[0].replace('N.º','Nº').split('Nº')[1].split(',')[1]
        Data_lei.append(result)
        
    elif 'O DIRETOR' in str(Texto_filtro[i]) and 'ISSN' not in str(Texto_filtro[i]) and 'Torna' not in str(Texto_filtro[i]) and 'Dispõe' not in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('O DIRETOR')[0].replace('N.º','Nº').replace('N°','Nº').split('Nº')[1].split(' ',3)[3].replace('  ','')
        Data_lei.append(result)
        
    elif 'Dispõe' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Dispõe')[0].replace('N.º','Nº').replace('N°','Nº').split('Nº')[1].split(',')[1].replace('  ','')
        Data_lei.append(result)
    
    elif 'Em atendimento' in str(Texto_filtro[i]):
        result = str(Texto_filtro[i]).split('Em atendimento')[0].replace('.','').replace('nº','Nº').replace('de','DE').split('Nº')[1].split(' ',2)[2].replace(',','')
        Data_lei.append(result)
        
    else: 
        Data_lei.append(' ')
        
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

# In[27]:


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

# In[28]:


import pandas as pd 

BANCO = pd.concat([BANCO_HTML,BANCO_PDF])
BANCO.to_csv("Portaria_Ancine.txt", index=False, encoding='utf-8-sig', sep = '汉')


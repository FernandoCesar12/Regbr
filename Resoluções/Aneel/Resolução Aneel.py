#!/usr/bin/env python
# coding: utf-8

# # Separando os links 

# In[45]:


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

url = "https://biblioteca.aneel.gov.br/Resultado/ListarLegislacao?guid=1642597687934"

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(url)

driver.implicitly_wait(30)

# Selecionando a opção de Legislação

select = driver.find_element_by_xpath('//*[@id="divBuscaRapida"]/li[1]/div/div[1]/button').click();
time.sleep(5)
    
select = driver.find_element_by_xpath('//*[@id="divBuscaRapida"]/li[1]/div/div[1]/ul/li[3]').click();
time.sleep(5)

# Selecionando as resoluções
    
select = driver.find_element_by_xpath('//*[@id="PalavraChave"]') # Digitando a parte textual
select.send_keys('Portaria') 
time.sleep(5)

select = driver.find_element_by_xpath('//*[@id="divBuscaRapida"]/li[1]/div/span/button').click(); # Apertando o botao de buscar
time.sleep(10)

select = driver.find_element_by_class_name('exibirFaceta').click(); # Exibindo todas as normas
time.sleep(5)

select = driver.find_element_by_xpath('//*[@id="content_Norma"]/div[20]').click(); # Exibindo todas as normas
time.sleep(20)

# Mostra mais

while True: 
    
    try:
        driver.find_element_by_id('btn-mostrar-mais-resultados').click();
        time.sleep(10)
        
    except:
        break
        
# Realizando a busca textual

time.sleep(20)

soup = BeautifulSoup(driver.page_source, 'lxml')
valores_p = soup.find_all('a', class_='link-detalhe')
result = ' '.join([str(elem) for elem in valores_p]).replace('amp;', '').split('</a>')

situacao = soup.find_all('p', class_='situacao')
assinatura = soup.find_all('p', class_='assinatura')
publicacao = soup.find_all('p', class_='publicacao')
link = soup.find_all('p', class_='sites')

situacao_href = ' '.join([str(elem) for elem in situacao]).split('</p>')
assinatura_href = ' '.join([str(elem) for elem in assinatura]).split('</p>')
publicacao_href = ' '.join([str(elem) for elem in publicacao]).split('</p>')

assinatura_final = []
for i in range(0,len(assinatura_href)-1):
    assinatura_final.append(str(assinatura_href[i]).split('</span>')[1].split('\n')[0])
    
situacao_final = []
for i in range(0,len(situacao_href)-1):
    if 'REVOGADA' in str(situacao_href[i]):
        situacao_final.append(True)
    else:
        situacao_final.append(False)
        
publicacao_final = []
for i in range(0,len(publicacao_href)-1):
    publicacao_final.append(str(publicacao_href[i]).split('</span>')[1].split('\n')[0])
    
    
Resolucao= []
for i in range(0,len(result)):
    if 'class="box-capa"' in str(result[i]):
        Resolucao.append(str(result[i]).split('REN')[1].split('" class=')[0])
        
Resolucao_nome = list(dict.fromkeys(Resolucao))
            
            
link_final = []

for i in range(0,len(link)):
    if 'Texto Integral' in str(link[i]):
        link_final.append(str(link[i]).split('href="')[1].split('" itemprop')[0])


# # Realizando a leitura dos PDF's

# In[47]:


# Entrando com os pacotes necessários

import io
import requests
from PyPDF2 import PdfFileReader
import re

#Selecionando a URL

url_list = link_final

Texto = []

for url in url_list:
    try:
        
        r = requests.get(url)
        f = io.BytesIO(r.content)

        reader = PdfFileReader(f)

        content = [] # Realizando o loop para pegar todas as páginas simultaneamente
        for page in range(0,reader.numPages):
            content.append(reader.getPage(page).extractText()) 
        
        Conteudo = ' '.join([str(elem) for elem in content])

        Texto.append(Conteudo.replace('\n','').replace('  ','').replace('JANEIRODE','JANEIRO DE').replace('FEVEREIRODE','FEVEREIRO DE').replace('MARÇODE','MARÇO DE').replace('ABRILDE','ABRIL DE').replace('MAIODE','MAIO DE').replace('JUNHODE','JUNHO DE').replace('JULHODE','JULHO DE').replace('AGOSTODE','AGOSTO DE').replace('AGOSTODE','AGOSTO DE').replace('SETEMBRODE','SETEMBRO DE').replace('OUTUBRODE','OUTUBRO DE').replace('NOVEMBRODE','NOVEMBRO DE').replace('DEZEMBRODE','DEZEMBRO DE'))
    except:
        Texto.append('')


# # Separando as variáveis

# In[66]:


import pandas as pd

# Criando o ID 

tipo = ['705']*len(Texto) # Tipo de Lei

Num_resolucao = []

for i in range(0,len(Resolucao_nome)):
    Num_resolucao.append(str(Resolucao_nome[i].split('NORMATIVA')[1].split('/')[0].replace(' ','')))
    
Ano_resolucao = []

for i in range(0,len(Resolucao_nome)):
    Ano_resolucao.append(str(Resolucao_nome[i].split('/')[1].replace(' ','')))
    
parte1 = [i + j for i, j in zip(tipo, Num_resolucao)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_resolucao)] 


# Criando um DataFrame para alocar os outputs

BANCO = pd.DataFrame (ID ,columns=['ID'])
BANCO['Texto_lei'] = Texto
BANCO['Data_lei'] = assinatura_final
BANCO['Data_publicação'] = publicacao_final
BANCO['Tipo_lei'] = tipo
BANCO['Revogada'] = situacao_final
BANCO['Setor'] = ['ANEEL']*len(Texto)

# Exportando em formato TXT

BANCO.to_csv("Resolucoes_Aneel.txt", index=False, encoding='utf-8-sig')

BANCO


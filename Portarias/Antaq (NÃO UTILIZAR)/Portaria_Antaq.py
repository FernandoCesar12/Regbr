#!/usr/bin/env python
# coding: utf-8

# # Separando os links para extração dos dados

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

url = "http://sophia.antaq.gov.br/terminal/Resultado/ListarLegislacao?guid=1614188149693"

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
select.send_keys('Resolução') 
time.sleep(5)

select = driver.find_element_by_xpath('//*[@id="divBuscaRapida"]/li[1]/div/span/button').click(); # Apertando o botao de buscar
time.sleep(10)

select = driver.find_element_by_class_name('exibirFaceta').click(); # Exibindo todas as normas
time.sleep(5)

select = driver.find_element_by_xpath('//*[@id="content_Norma"]/div[17]').click(); # Exibindo todas as normas
time.sleep(10)

select = driver.find_element_by_xpath('//*[@id="content_ConteudoDigital"]/div[1]/label').click(); # Exibindo todas as normas
time.sleep(10)


select = driver.find_element_by_xpath('//*[@id="content_Assunto"]/div[1]/label').click(); # Exibindo todas as normas
time.sleep(10)


select = driver.find_element_by_xpath('//*[@id="btn-visualizacao-capa"]').click();
time.sleep(5)

# Mostra mais

while True: 
    
    try:
        driver.find_element_by_id('btn-mostrar-mais-resultados').click();
        time.sleep(5)
        
    except:
        break
        
# Realizando a busca textual

soup = BeautifulSoup(driver.page_source, 'lxml')
valores_p = soup.find_all('p', class_='titulo')
result = ' '.join([str(elem) for elem in valores_p]).replace('amp;', '').split('</p>')

link = []
for i in range(0,len(result)):
    if 'href="' in result[i]:
        resultado = result[i].split('href="')[1].split('">')[0]
        
        if '" ' in resultado:
            resultado2 = resultado.split('" ')[0]
            link.append(resultado2)
        else:
            link.append(resultado)
            
            
append_str = 'http://sophia.antaq.gov.br'
link_append = [append_str + sub for sub in link]  # Adicionando o préfixo

link_resolucoes = list(dict.fromkeys(link_append))


# # Separando as informações textuais

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


import time
import re

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

url_list = link_resolucoes

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

############################################## Separando a Data de Publicação DOU e Revogação

Resultado_lista_2 = []
valores_resolucao = []

for url in url_list:
    
    try:
        
        driver.get(url)

        driver.implicitly_wait(10)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        valores_resolu = soup.find_all('h1', class_='titulo')
        valores_resolucao.append(valores_resolu)
    
        valores_p = soup.find_all('div', class_='col-xs-12 col-sm-9 col-lg-10')
        Resultado_lista_2.append(valores_p)
        
    except:
        print('Página não encontrada')

# Resultado_lista = [item for sublist in Resultado_lista_2 for item in sublist]

# Revogação

Revogado = []

for i in range(0,len(Resultado_lista_2)):
    
    try:
        
        if 'Situação' in str(Resultado_lista_2[i]) and 'Revogado' in str(Resultado_lista_2[i]):
            result = True
            Revogado.append(result)
    
        else:
            result = False
            Revogado.append(result)
        
    except:
    
        Revogado.append('')
        
# Data de Publicação

Data_publica = []

for i in range(0,len(Resultado_lista_2)):
    try:
        if 'datePublished' in str(Resultado_lista_2[i]):
            result  = str(Resultado_lista_2[i]).split('datePublished">')[1].split('</p>')[0]
            Data_publica.append(result)
            
        else:
            result = ''
            Data_publica.append(result)
    
    except:
    
        Data_publica.append('')
        
        
# Data da assinatura

Data_resolucao = []

for i in range(0,len(Resultado_lista_2)):
    
    try: 
        
        if 'Data de assinatura' in str(Resultado_lista_2[i]):
            result  = str(Resultado_lista_2[i]).split('legislationDate">')[1].split('</p>')[0]
            Data_resolucao.append(result)
        
        else:
            Data_resolucao.append('')
            
    except:
        
        Data_resolucao.append('')
        
# Pegando o Título da portaria

titulo = []
for i in range(0,len(valores_resolucao)):
    
    try:
        result = str(valores_resolucao[i]).split('itemprop="name">')[1].split('</h1>')[0]
        titulo.append(result)
        
    except:
        titulo.append('')
        
        
# Ano da resolução

Ano_resolucao = []

for i in range(0,len(titulo)):
    
    try:
        result = titulo[i][-4:]
        
        if len(str(result).replace(' ','')) == 4:
            Ano_resolucao.append(result)
        
        else:
            Ano_resolucao.append('')
            
    except:
        Ano_resolucao.append("")
        
        
# Número da portaria

Num_resolu = []

for i in range(0,len(titulo)):
    
    try:
        result = titulo[i].split('DG ')[1]
        
        if '/' in str(result):
            Num_resolu.append(str(result).split('/')[0])
        
        else:
            Num_resolu.append(str(result).split('-')[0].replace(' ',''))

        
    except:
        Num_resolu.append("")
        
for i in range(0,len(Num_resolu)):
        
    if '-' in Num_resolu[i]:
        Num_resolu[i] = Num_resolu[i].split('-')[0]
        
############################################## Pegando a parte textual

Texto = []

for url in url_list:
    
    try:
        
        driver.get(url)

        driver.implicitly_wait(10)
    
        select = driver.find_element_by_class_name('texto-exibir-mais').click(); 
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        texto_sem_formatacao = soup.find_all('div', class_='col-xs-12')
        texto_com_formatacao = re.sub('\<(.*?)\>','',str(texto_sem_formatacao), flags=re.DOTALL).replace('\n','').replace('\t','').replace('\xa0','')
        Texto.append(texto_com_formatacao)
        
    except:
        
        print('Texto não encontrado')
        Texto.append('')


# In[3]:


# Criando o ID 

tipo = ['809']*len(Texto) # Tipo de Lei

parte1 = [i + j for i, j in zip(tipo, Num_resolu)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_resolucao)] 

for i in range(0,len(ID)):
    ID[i] = ID[i].replace(' ','')

# Limpando a variável texto

texto_final = []

for i in range(0,len(Texto)):
    texto_final.append(Texto[i].replace(' Voltar , SelecionarFavoritar, SelecionarFavoritar, ',''))
    
# Criando um DataFrame para alocar os outputs

import pandas as pd

BANCO = pd.DataFrame (ID ,columns=['ID'])
BANCO['Texto_lei'] = texto_final
BANCO['Data_lei'] = Data_resolucao
BANCO['Data_publicação'] = Data_publica
BANCO['Tipo_lei'] = tipo
BANCO['Revogada'] = Revogado
BANCO['Setor'] = ['Antaq']*len(Texto)

BANCO


# In[4]:


BANCO.to_csv("Portaria_Antaq.txt", index=False, encoding='utf-8-sig', sep = '汉')


#!/usr/bin/env python
# coding: utf-8

# # Pegando os links dos PDF's

# In[1]:


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

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

link_pdf = []

links_ano = ['http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/quadro_emc.htm']

for url in links_ano:
    
    driver.get(url)

    driver.implicitly_wait(5)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    href = ' '.join([str(elem) for elem in soup]).split('valign="top" width="29%')

    link_pdf_ano = []

    for i in range(0,len(href)):
        if '<small>' in str(href[i]) and 'href=' in str(href[i]):
            result = str(href[i]).split('href="')[1].split('">')[0]
            link_pdf_ano.append(result)
        
    link_pdf.append(link_pdf_ano)
    
# Transformando numa única lista 

flat_list_pdf = [item for sublist in link_pdf for item in sublist]
            
append_str = 'http://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/'
link_resolucoes = [append_str + sub for sub in flat_list_pdf]  # Adicionando o préfixo


# # Pegando o conteudo textual e o link de redirecionamento

# In[7]:


import re 

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

Conteudo_textual = []
Conteudo_link = []

for url in link_resolucoes:
    
    try:
        
        driver.get(url)

        driver.implicitly_wait(5)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')
    
        Conteudo = soup.find_all('p')
    
        texto = re.sub("[\<\[].*?[\>\]]", "", str(Conteudo)).replace('\n','').replace(', \xa0','')
    
        Link = str(soup.find_all('a')).split('href="')[1].split('">')[0]
    
        Conteudo_textual.append(texto)
    
        Conteudo_link.append(Link)
        
    except:
        
        print(f'Erro de leitura no link: {url}')
        


# # Extraindo informações adicionais

# In[10]:


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

Data_assinatura = []
Ementa = []
Situacao = []
Chefe_governo = []
Origem = []
Data_publicacao = []
Fonte = []
Referenda = []
Alteracao = []
Veto = []
Assunto = []
Classificacao_direito = []
Observacao = []
Correlacao = []
Titulo = []
error_site = []

for url in Conteudo_link:
    
    try:
        
        driver.get(url)

        driver.implicitly_wait(5)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')
    
        items_titulo = soup.find_all("h1", {"class": "text-center font-weight-bold title text-uppercase"})
        Titulo.append(str(items_titulo[0]).split('text-uppercase">')[1].split('</h1>')[0])
    
        items = soup.find_all("li", {"class": "list-group-item border-0 p-0"})
        href = ' '.join([str(elem) for elem in items]).split('<div class="col-sm-2 label p-2">')

        #Separando as informações textuais
    
        for i in range(0,len(href)):
            try:
                if 'Data de assinatura:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Data_assinatura.append(result)
            except:
                Data_assinatura.append('')
            
    
        for i in range(0,len(href)):
            try:
                if 'Ementa:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Ementa.append(result)
            except:
                Ementa.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Situação:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Situacao.append(result)
            except:
                Situacao.append('')
            
    
        for i in range(0,len(href)):
            try:
                if 'Chefe de Governo:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Chefe_governo.append(result)
            except:
            
                Chefe_governo.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Origem:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Origem.append(result)
            except:
            
                Origem.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Data de Publicação:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Data_publicacao.append(result)
            except:
            
                Data_publicacao.append('')
            
    
        for i in range(0,len(href)):
            try:
                try:
                    if 'Fonte:' in str(href[i]):
                        result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','').split('href="')[1].split('" target=')[0].replace('amp;','')
                        Fonte.append(result)
            
                except:
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','').replace('amp;','')
                    Fonte.append(result)
            except:
                Fonte.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Referenda:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Referenda.append(result)
            except:
                Referenda.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Alteração:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Alteracao.append(result)
            except:
                Alteracao.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Correlação:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Correlacao.append(result)
            except:
                Correlacao.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Veto:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Veto.append(result)
            except:
                Veto.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Assunto:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Assunto.append(result)
            except:
                Assunto.append('')
    
        for i in range(0,len(href)):
            try:
                if 'Classificação de direito:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Classificacao_direito.append(result)
            except:
                Classificacao_direito.append('')
        
    
        for i in range(0,len(href)):
            try:
                if 'Observação:' in str(href[i]):
                    result = str(href[i]).split('text-justify">')[1].split('/div>')[0].replace('\t','').replace('\n','').replace('  ','').replace('<','').replace('br/>','')
                    Observacao.append(result)
            except:
                Observacao.append('')
                
    except:
        
        error_site.append(url)
        print(f'Erro na obtenção dos dados referentes ao link: {url}')
        
# Realizando a limpeza dos links com problemas

links_indice = []

for i in range(0,len(error_site)):
    
    result = Conteudo_link.index(error_site[i])
    links_indice.append(result)

# Removendo os links

for i in range(0,len(links_indice)):
        
    del Conteudo_link[links_indice[i]]
    
# Removendo o conteudo textual

for i in range(0,len(links_indice)):
        
    del Conteudo_textual[links_indice[i]]


# # Exportando em CSV

# In[15]:


# Criando um DataFrame para alocar os outputs

import pandas as pd

BANCO = pd.DataFrame (Titulo ,columns=['Decreto-Lei'])
BANCO['Link'] = Conteudo_link
BANCO['Texto'] = Conteudo_textual
BANCO['Data de assinatura'] = Data_assinatura
BANCO['Ementa'] = Ementa
BANCO['Situação'] = Situacao
BANCO['Chefe de Governo'] = Chefe_governo
BANCO['Origem'] = Origem
BANCO['Data de publicação'] = Data_publicacao
BANCO['Fonte'] = Fonte
BANCO['Referenda'] = Referenda
BANCO['Alteração'] = Alteracao
BANCO['Veto'] = Veto
BANCO['Classificação de direito'] = Classificacao_direito
BANCO['Observação'] = Observacao
BANCO['Correlação'] = Correlacao

# Removendo páginas bloqueadas pelo governo 

BANCO = BANCO[BANCO['Texto'] != ']']

excelfilename = 'Emenda_constitucional'+ time.strftime("%d-%m-%Y") +".csv"

BANCO.to_csv(excelfilename, index=False, encoding='utf-8-sig', sep = '汉')


# In[17]:


BANCO


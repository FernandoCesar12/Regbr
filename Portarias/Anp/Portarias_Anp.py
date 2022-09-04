#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das páginas redirecionadas

# In[22]:


import requests # requisições web
import re
from bs4 import BeautifulSoup

Link = []
i  = 1
while i <= 35:
  try:
    url = 'https://atosoficiais.com.br/anp?q=&types=153&types=183&page=34&page='+str(i)

    header = {'User-Agent': "'Mozilla/5.0'"}
    html = requests.get(url, headers = header)
    bs_obj = BeautifulSoup(html.text,"lxml")
    posicao = bs_obj.find_all("div", {"class": "listagem-leis"})
    hrefs = ' '.join([str(elem) for elem in posicao]).split('\n')

    for href in hrefs:
      if '<a class="btn btn-lei-lista"' in str(href):
        result = str(href).split('href="')[1].split('">')[0]
        Link.append(result)

    i = i+1

  except:
    print('Url error' + ' ' + url)

# Finalizando a formatação as URL's

append_str = 'https://atosoficiais.com.br'
Links_portarias = [append_str + sub for sub in Link]  # Adicionando o préfixo


# # Realizando a estração TEXTUAL

# In[24]:


url_list = Links_portarias # Entrando com a lista de URL's em interesse

Texto = []
Titulo = []

for url in url_list :
    try:
        header = {'User-Agent': "'Mozilla/5.0'"}
        html = requests.get(url, headers = header)
        bs_obj = BeautifulSoup(html.text,"lxml")
        posicao = bs_obj.find_all("div", {"id": "conteudo-principal"})

        hrefs = ' '.join([str(elem) for elem in posicao]).split('\n')

        Resultado = []
        for i in range(0,len(hrefs)): # Separando a parte textual em interesse
            if 'class="text-center"' in hrefs[i]:
                Resul = hrefs[i].split('<center>',1)[1]
                Resultado.append(Resul)

        for i in range(0,len(Resultado)): # Separando o título
            title =  Resultado[i].split('<h2>',1)[1].split('</h2>',1)[0]
            Titulo.append(title)

        for i in range(0,len(Resultado)):  # Separando o título
            text = Resultado[i].split('</h2>',1)[1].split('</i></p>',1)[0].replace('</h1>','').replace('<br/>','').replace('<h1>','').replace('<br>','')
            Texto.append(text)
            
    except:
        print('Erro')


# In[25]:


Tipo = ['807']*len(Titulo) # Tipo de Lei

Ano_lei = [] # Pegando o ano da lei

for i in range(0,len(Titulo)):
    
    if '/' not in str(Titulo[i]):
        
        ano = Titulo[i].split('DE',1)[1].split('-',1)[0]
        if ',' in Titulo[i]:
            Ano_lei.append(ano.split(',',1)[0])
        
        else: 
            Ano_lei.append(ano)
            
    else:
        Ano_lei.append(Titulo[i].split('/',1)[1].replace('.',''))

     
ano_lei_2 = []
for i in range(0,len(Ano_lei)):
    result = Ano_lei[i].replace(' ','').replace('(*)','').replace('.','')[-4:]
    ano_lei_2.append(result)
    
    
Num_lei_1 = [] # Pegando o número da lei
for i in range(0,len(Titulo)):
    
    try:
        if 'Nº' in str(Titulo[i]):
            ano = Titulo[i].split(',',1)[0].split('Nº',1)[1].replace('P','').replace('Nº','').replace('º','').replace(' ','').replace('n','')
            Num_lei_1.append(ano)
        
        else: 
            ano = Titulo[i].split(',',1)[0].split('N',1)[1].replace('P','').replace('Nº','').replace('º','').replace(' ','').replace('n','')
            Num_lei_1.append(ano)
            
    except:
        
        ano = Titulo[i].split(',',1)[0].split(' ',1)[1]
        Num_lei_1.append(ano)
        
Num_lei = []

for i in range(0,len(Num_lei_1)):
    
    if '/' in str(Num_lei_1[i]):
        
        result = str(Num_lei_1[i]).split('/',1)[0]
        Num_lei.append(result)
        
    elif '-' in str(Num_lei_1[i]):
        
        result = str(Num_lei_1[i]).split('-',1)[0]
        Num_lei.append(result)
        
    else:
        
        result = str(Num_lei_1[i])
        Num_lei.append(result)
        
parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano_lei_2)] 

################################################ Data_publicação

Data_DOU = [] # Pegando a data de publicação no DOU

for i in range(0,len(Titulo)):
    if '/' not in str(Titulo[i]):
        ano = Titulo[i].split("DE ",1)[1].replace('(*)','').replace('-','').replace(',','')
        Data_DOU.append(ano)
    else:
        ano = Titulo[i].split('/',1)[1].replace('.','')
        Data_DOU.append(ano)

Data_DOU_limpeza_1 = []

for i in range(0,len(Data_DOU)):
    
    try: 
        
        if 'DOU' in str(Data_DOU[i]):
            limpeza = str(Data_DOU[i]).split("DOU",1)[0].replace('  ','').replace('RETIFICADA','')
            Data_DOU_limpeza_1.append(limpeza)
        

        
        elif ',' in str(Data_DOU[i]):
            limpeza = str(Data_DOU[i]).split(",",1)[0]
            Data_DOU_limpeza_1.append(limpeza)
        
        elif ')' in str(Data_DOU[i]):
            limpeza = str(Data_DOU[i]).split(")",1)[0].split('DE',2)[2]
            Data_DOU_limpeza_1.append(limpeza)
        
        else:
            Data_DOU_limpeza_1.append(Data_DOU[i])         
            
    except:
        Data_DOU_limpeza_1.append(' ')
        
Data_DOU_limpeza_2 = []

for i in range(0,len(Data_DOU_limpeza_1)):
    if len(str(Data_DOU_limpeza_1[i])) <= 30:
        Data_DOU_limpeza_2.append(Data_DOU_limpeza_1[i])
    else:
        Data_DOU_limpeza_2.append(' ')

################################################ Revogada

Resultado_revoga = []
for i in range(0,len(Texto)):
    if 'REVOGADA' in str(Texto[i]).upper():
        result = True
        Resultado_revoga.append(result)
    else:
        result = False
        Resultado_revoga.append(result)

import pandas as pd

# Criando um DataFrame para alocar os outputs

dados = pd.DataFrame (ID ,columns=['ID'])
dados['Texto_lei'] = Texto
dados['Data_lei'] = Ano_lei
dados['Data_publicação'] = Data_DOU_limpeza_2
dados['Tipo_lei'] = Tipo
dados['Revogada'] = Resultado_revoga
dados['Setor'] = ['Anp']*len(Titulo)


# In[26]:


dados


# In[30]:


# Exportando em formato TXT

dados.to_csv("Portarias_Anp.txt", index=False, encoding='utf-8-sig', sep = '汉')


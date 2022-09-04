#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das páginas redirecionadas

# In[1]:


import requests # requisições web
import re
from bs4 import BeautifulSoup

pattern = r"\/anp\/resolucao-n-\d+-\d+"

Link = []
i  = 1
while i <= 90:
  try:
    url = 'https://atosoficiais.com.br/anp?q=&types=24&types=156&page='+str(i)

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
link_resolucoes = [append_str + sub for sub in Link]  # Adicionando o préfixo


# # Pegando a parte textual

# In[2]:


url_list = link_resolucoes # Entrando com a lista de URL's em interesse

Texto = []
Titulo = []

for url in url_list :
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


# # Criando o banco de Dados Brutos

# In[74]:


################################################ Criando o ID

Tipo = ['707']*len(Titulo) # Tipo de Lei

Ano_lei = [] # Pegando o ano da lei

for i in range(0,len(Titulo)):
  ano = Titulo[i].split('DE',1)[1].split('-',1)[0]
  if ',' in Titulo[i]:
    Ano_lei.append(ano.split(',',1)[0])
    
  else: 
    Ano_lei.append(ano)

ano_lei_2 = []
for i in range(0,len(Ano_lei)):
  result = Ano_lei[i].replace(' ','').replace('(*)','').replace('.','')[-4:]
  ano_lei_2.append(result)
    

Num_lei = [] # Pegando o número da lei
for i in range(0,len(Titulo)):
    
    if 'Nº' in str(Titulo[i]):
      ano = Titulo[i].split(',',1)[0].split('Nº',1)[1].replace('P','').replace('Nº','').replace('º','').replace(' ','')
      Num_lei.append(ano)
        
    else: 
        ano = Titulo[i].split(',',1)[0].split('N',1)[1].replace('P','').replace('Nº','').replace('º','').replace(' ','')
        Num_lei.append(ano)

parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano_lei_2)] 

################################################ Data_publicação

Data_DOU = [] # Pegando a data de publicação no DOU

for i in range(0,len(Titulo)):
    ano = Titulo[i].split("DE ",1)[1].replace('(*)','').replace('-','').replace(',','')
    Data_DOU.append(ano)
 
Data_DOU_limpeza_1 = []

for i in range(0,len(Data_DOU)):
    if 'DOU' in str(Data_DOU[i]):
        limpeza = str(Data_DOU[i]).split("DOU",1)[0].replace('  ','')
        Data_DOU_limpeza_1.append(limpeza)


################################################ Revogada

Resultado_revoga = []
for i in range(0,len(Link)):
  if 'Norma revogada' in Link[i]:
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
dados['Data_publicação'] = Data_Dou
dados['Tipo_lei'] = Tipo
dados['Revogada'] = Resultado_revoga
dados['Setor'] = ['Anp']*len(Titulo)


# In[77]:


dados.to_csv("Resolucao_ANP.txt", index=False, encoding='utf-8-sig', sep = '汉')


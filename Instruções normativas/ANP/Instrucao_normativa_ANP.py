#!/usr/bin/env python
# coding: utf-8

# # Pegando os links das páginas redirecionadas

# In[1]:


import requests # requisições web
import re
from bs4 import BeautifulSoup

Link = []
i  = 1
while i <= 6:
  try:
    url = 'https://atosoficiais.com.br/anp?q=&types=202&types=203&types=204&types=200&types=201&types=9&page='+str(i)

    header = {'User-Agent': "'Mozilla/5.0'"}
    html = requests.get(url, headers = header)
    bs_obj = BeautifulSoup(html.text,"lxml")
    posicao = bs_obj.find_all("a")
    hrefs = ' '.join([str(elem) for elem in posicao]).split('<span rel="title">')

    for href in hrefs:
        if '<a class="btn btn-lei-lista"' in str(href):
            result = str(href).split('<a class="btn btn-lei-lista" href="')[1].split('">')[0]
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

# In[3]:


Titulo


# In[4]:


Titulo[i]


# In[5]:


Data_lei = [] # Pegando a data de publicação no DOU

for i in range(0,len(Titulo)):
    if 'DATA DE VIGÊNCIA' in str(Titulo[i]):
        ano = Titulo[i].split("DATA DE VIGÊNCIA")[1].split("-")[0].replace('DE','').replace(' ','').replace(',APROVAÇÃORESOLUÇÃODIRETORIANºRDNº135/2010',' ')
        Data_lei.append(ano)
    else:
        Data_lei.append(' ')
 
Data_lei


# In[6]:


################################################ Criando o ID

Tipo = ['707']*len(Titulo) # Tipo de Lei

Num_lei = [] # Pegando o ano da lei

for i in range(0,len(Titulo)):
    if ', DE' not in str(Titulo[i]):
        Num_lei.append(Titulo[i].split('Nº ')[1].split('/')[0])
        
    elif ', DE' in str(Titulo[i]):
        Num_lei.append(Titulo[i].split('Nº ')[1].split(', DE')[0].replace('/2012, DATA DA VIGÊNCIA 01/02/2012- APROVAÇÃO RD ',''))

        
Ano_lei = [] # Pegando o ano da lei

for i in range(0,len(Titulo)):
    Ano_lei.append(Titulo[i][-4:].replace('6/99','1999').replace('2/99','1999'))

parte1 = [i + j for i, j in zip(Tipo, Num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, Ano_lei)] 

################################################ Data_publicação

Data_DOU = [] # Pegando a data de publicação no DOU

for i in range(0,len(Titulo)):
    if 'DOU' in str(Titulo[i]):
        ano = Titulo[i].split("DOU")[1].replace('DE','').replace(' ','').replace('JANEIRO','.01.').replace('FEVEREIRO','.02.')
        Data_DOU.append(ano)
    else:
        Data_DOU.append(' ')

################################################ Data_lei

Data_lei = [] 

for i in range(0,len(Titulo)):
    if 'DATA DE VIGÊNCIA' in str(Titulo[i]):
        ano = Titulo[i].split("DATA DE VIGÊNCIA")[1].split("-")[0].replace('DE','').replace(' ','').replace(',APROVAÇÃORESOLUÇÃODIRETORIANºRDNº135/2010',' ')
        Data_lei.append(ano)
    else:
        Data_lei.append(' ')

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
dados['Data_lei'] = Data_lei
dados['Data_publicação'] = Data_DOU
dados['Tipo_lei'] = Tipo
dados['Revogada'] = Resultado_revoga
dados['Setor'] = ['Anp']*len(Titulo)

dados


# In[7]:


dados.to_csv("Instrucao_normativa_ANP.txt", index=False, encoding='utf-8-sig', sep = '汉')


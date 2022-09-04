#!/usr/bin/env python
# coding: utf-8

# # Pegando os links referente aos anos

# In[1]:


import requests # requisições web
import re
from bs4 import BeautifulSoup

url = "https://www.anatel.gov.br/legislacao/resolucoes" # coloca o site que pretende fazer web scrapping
header = {'User-Agent': "'Mozilla/5.0'"}
html = requests.get(url, headers = header)
bs_obj = BeautifulSoup(html.text,"lxml")
posicao = bs_obj.find_all('a') # você coloca a posição que ele se encontra na página

pattern = r"\/legislacao\/resolucoes\/\d+"
hrefs = str(posicao).split(",")

years = [] 
for href in hrefs:
  result = re.search(pattern, href)
  if result != None:
    years.append(result.group())

years_duplicadas = list(dict.fromkeys(years))

# Adicionando um préfixo
append_str = 'https://www.anatel.gov.br'
link_years = [append_str + sub for sub in years_duplicadas]

link_years


# # Pegando os links presentes em todos os anos

# In[2]:


url_list = link_years # coloca o site que pretende fazer web scrapping

pattern = r"\/legislacao\/resolucoes\/\d+\/\d+-resolucao-\d+"

Revoga = []
resolucao = [] 
resolucoes_list = []

for url in url_list:

  header = {'User-Agent': "'Mozilla/5.0'"}
  html = requests.get(url, headers = header)
  bs_obj = BeautifulSoup(html.text,"lxml")
  posicao = bs_obj.find_all('a') # você coloca a posição que ele se encontra na página

  hrefs = str(posicao).split(",")


  for href in hrefs:
    result = re.search(pattern, href)
    if result != None:
      resolucao.append(result.group())
      Revoga.append(href)

  resolucao_duplicadas = list(dict.fromkeys(resolucao))

# Adicionando um préfixo
append_str = 'https://www.anatel.gov.br'
link_resolucoes = [append_str + sub for sub in resolucao_duplicadas]


# # Realizando a Leitura dos arquivos via HTML

# In[17]:


url_list = link_resolucoes
Texto_list = []
Titulo_list = []

for url in url_list:

  header = {'User-Agent': "'Mozilla/5.0'"}
  html = requests.get(url, headers = header)
  bs_obj = BeautifulSoup(html.text,"lxml").text

  if 'Voltar ao topo' in bs_obj:
    texto = bs_obj.replace('  ','').replace('\n','').replace('\xa0','').replace('\t','').replace('\r','').split('Voltar ao topo')[0]
    Texto_list.append('Resolução' + texto)
    
  else:
    texto = ''
    Texto_list.append(texto)

  if 'Publicado' in bs_obj:
    titulo_separado = texto.split('Publicado')[0].split('\ufeff')[0].split('Legislação')[0].replace('}','').split('Agência')[0]
    titulo = 'Resolução'+titulo_separado
    Titulo_list.append(titulo)

  else:
    titulo = ''
    Titulo_list.append(titulo)


# # Criando o banco de Dados Brutos

# In[48]:


################################################ Criando o ID

tipo = ['703']*len(Titulo_list) # Tipo de Lei

ano_lei_1 = []

for i in range(0,len(Titulo_list)):
  
    if 'REVOGADA' in str(Titulo_list[i]) and ',' in str(Titulo_list[i]):
        result = str(Titulo_list[i]).split(',')[1].split(' (')[0][4:].replace('(REVOGADA)Anatel - ','')
        ano_lei_1.append(result)
        
    elif ',' not in str(Titulo_list[i]) and 'REVOGADA' in str(Titulo_list[i]):
        
        result = str(Titulo_list[i]).split('nº')[1].split(' (')[0][4:].replace('(REVOGADA)Anatel - ','')[4:]
        ano_lei_1.append(result)
    
    elif ',' not in str(Titulo_list[i]) and 'REVOGADA' not in str(Titulo_list[i]):
        
        result = Titulo_list[i].split('Anatel -')[1][20:]
        ano_lei_1.append(result)
        
    else:
        
        result = Titulo_list[i].split('Anatel -')[1].split(',')[1][4:].replace(' (da SCP)','')
        ano_lei_1.append(result)
        
ano_lei = []

for i in range(0,len(ano_lei_1)):      
    
    if '(' in str(ano_lei_1[i]):
        ano_lei.append((str(ano_lei_1[i]).split('(')[0])[-4:])
    else:
        ano_lei.append((ano_lei_1[i])[-4:])
        

num_lei_1 = [] # Pegando o numero da lei
for i in range(0,len(Titulo_list)):
    result = Titulo_list[i].split('n')[2].split(',')[0].replace(' ','').replace('º','')
    num_lei_1.append(result)
    
num_lei = [] 
for i in range(0,len(num_lei_1)):
    if 'de' in str(num_lei_1[i]):
        result = num_lei_1[i].split('de')[0]
        num_lei.append(result)
    else:
        num_lei.append(num_lei_1[i].replace('o','0'))

parte1 = [i + j for i, j in zip(tipo, num_lei)] # Juntado os valores
ID = [i + j for i, j in zip(parte1, ano_lei)] 


################################################ Data_lei

Data_lei_1 = []

for i in range(0,len(Titulo_list)):
  
    if 'REVOGADA' in str(Titulo_list[i]) and ',' in str(Titulo_list[i]):
        result = str(Titulo_list[i]).split(',')[1].split(' (')[0][4:].replace('(REVOGADA)Anatel - ','')
        Data_lei_1.append(result)
        
    elif ',' not in str(Titulo_list[i]) and 'REVOGADA' in str(Titulo_list[i]):
        
        result = str(Titulo_list[i]).split('nº')[1].split(' (')[0][4:].replace('(REVOGADA)Anatel - ','')[4:]
        Data_lei_1.append(result)
    
    elif ',' not in str(Titulo_list[i]) and 'REVOGADA' not in str(Titulo_list[i]):
        
        result = Titulo_list[i].split('Anatel -')[1][20:]
        Data_lei_1.append(result)
        
    else:
        
        result = Titulo_list[i].split('Anatel -')[1].split(',')[1][4:].replace(' (da SCP)','')
        Data_lei_1.append(result)
        
Data_lei = []

for i in range(0,len(Data_lei_1)):      
    
    if '(' in str(Data_lei_1[i]):
        Data_lei.append((str(Data_lei_1[i]).split('(')[0]))
    else:
        Data_lei.append((Data_lei_1[i]))

################################################ Data_publicação

Data_publica = []
for i in range(0,len(Texto_list)):
  if 'Publicado' in Texto_list[i]:
    data = Texto_list[i].split('Publicado:', 1)[1].split('|Última atualização:', 1)[0][:-5]
    Data_publica.append(data)
  else:
    data = 'NA'
    Data_publica.append(data)

################################################ Revogada

Resultado_revoga = []
for i in range(0,len(Titulo_list)):
  if 'REVOGADA' in Titulo_list[i]:
    result = True
    Resultado_revoga.append(result)
  else:
    result = False
    Resultado_revoga.append(result)



import pandas as pd

# Criando um DataFrame para alocar os outputs

dados = pd.DataFrame (ID ,columns=['ID'])
dados['Texto_lei'] = Texto_list
dados['Data_lei'] = Data_lei
dados['Data_publicação'] = Data_publica
dados['Tipo_lei'] = tipo
dados['Revogada'] = Resultado_revoga
dados['Setor'] = ['Anatel']*len(Texto_list)

dados = dados[dados.ID.apply(lambda x: x.isnumeric())]


# In[49]:


dados


# In[50]:


dados.to_csv("Resolucao_ANATEL.txt", index=False, encoding='utf-8-sig')


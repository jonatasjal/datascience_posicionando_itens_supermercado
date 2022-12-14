# -*- coding: utf-8 -*-
"""[Jonatas-Liberato]posicionamento-itens-supermercado.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EhZkNrwGdn7207wTsURxSZDq0fBVQj0c

# **ANÁLISE DE POSICIONAMENTO DE ITENS EM SUPERMERCADOS**

# Sobre o Problema

Mais um projeto com o objetivo de aprimorar conhecimento e neste caso, faremos uma análise da cesta/carrinho de supermercado, com o objetivo de posicionar itens pelos corredores de um supermercado.

Neste projeto, também, estudaremos a **MINERAÇÃO REGRAS DE ASSOCIAÇÃO**, técnica essa usada para identificar possíveis relações entre itens diferente.

Algo muito comum nos supermercado. Onde foi identificado um padrão do costume de compras dos consumidores.

O objetivo disso é otimizar os lucros e evitar desperdícios. Posicionando os produtos de forma adequada nas prateleiras dos supermercados.

=======================================

1. **Exemplo:** 
- Homens: compram cervejas, petiscos, etc.
- Mulheres: compram comida para bebê, leite, fraldas, etc.

--

2. **Exemplo**: a velha história das pessoas que entraram no supermercado para comprar fraldas e se depararam com a proximidade de cervejas no corredor.

Matéria completa: [AQUI](https://exame.com/revista-exame/o-que-cerveja-tem-a-ver-com-fraldas-m0053931/)

# Benefícios

**Como a empresa/establecimento pode se beneficiar com o nosso sistema?**

Algumas das possibilidades mais importantes,são:
- Aquisição de mais produtos, correlacionados se estiverem próximos um dos outros
- Direcionamento de consumidores para adquirir outros produtos através de campanhas de marketing, por exemplo
- Ação promocional se o cliente comprar ambos produtos juntos

# O que será aplicado

Neste projeto, uma das principais técnicas utilizadas será a do **Algoritmo a Priori**.

Esse algoritmo de Machine Learning é muito útil para se obter informações sobre relacionamentos estruturados entre diferentes produtos ou itens envolvidos.

Esse algoritmo é muito usado para recomendação de produtos com base em outros já existentes no carrinho do usuário ou histórico de compras.

===================

Modo de usar:

Ele recebe 3 parâmetros essenciais em sua aplicação:
- **Suport** (suporte)
- **Confidence** (confiança)
- **Lift** (elevação)

===================

**Exemplo de aplicabilidade:**

Em um registro com 1000 transações, queremos descobrir os 3 parâmetros no caso de vendas de chuteiras e meiões.

Dentre essas 1000 transações, 200 foram de meiões e 200 de chuteiras. Dentre essas 200 transações de chuteiras, 180 tinham meiões inclusos.

Ou seja:

* **SUPORTE**

Suporte é a popularidade padrão de um determinado item e que pode ser calculado: dividindo-se o número de transações de um determinado item, pelo número total de transações. **Exemplo**: 200(chuteiras) / 1000 = 20%

* **CONFIANÇA**

É a probabilidade de um item ser comprado juntamento com outro e pode ser calculado através da divisão do número de transações em que ambos são comprados juntos, peo total de transações de um determinado item.
**Exemplo**: 180 (chuteiras e meiões) / 200 (chuteiras) = 90%

* **ELEVAÇÃO**

Refere-se ao aumento da razão de venda de um item, quando outro item é vendido. É calculado dividindo-se a **confiança** e o **suporte**.
**Exemplo**: 90 / 20 = 4,5


Conclusão: a probabilidade de alguém comprar o meião depois de ter comprado a chuteira, é 4,5 vezes maior do que comprar somente o meião.

**Regra**

Caso o aumento seja:

- **IGUAL** a 1, significa que não há associação entre os podutos
- **MAIOR** que 1, significa que existem probabilidades de serem comprados juntos
- **MENOR** que 1, é improvável que sejam comprados juntos

# Passo a Passo

1. Definir valor mínimo para **suporte** e **confiança** (ou seja, queremos encontrar regras para os itens que já possuam certa existência padrão e que possuam um valor mpinimo para coocorrência com outros itens.

2. **Extraia** todos os subconjuntos com valor de suporte mais alto que o limite mínimo

3. Selecione **todas as regras** dos subconjuntos com valor de confiança superior ao limite mínimo

4. Ordene as regras por ordem descrecente de **Lift**

# DATASET


Baixe [AQUI](https://www.dropbox.com/s/8987kdylqcyroxr/Market_Basket_Optimisation.csv?dl=0)

# BIBLIOTECAS
"""

# Algoritmo a priori
!pip install apyori

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""# 1 - ANÁLISE EXPLORATÓRIA"""

# Importando dataset
dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)
dataset

dataset.shape

"""# 2 - PRÉ-PROCESSAMENTO

*Descobrimos que o dataset tem mais de 7500 transações e nós decidimos que a quantidade de produtos que usaremos nas análise e limitaremos até 20 produtos.*
"""

transacoes = []
for i in range(0, 7501):
  transacoes.append([str(dataset.values[i,j]) for j in range(0, 20)])
  
transacoes

"""*Esse procedimento fez nada mais que separar as compras de cada cliente em uma lista.*"""

# transformando em uma lista
transacoes_lista = dataset.values.tolist()

for i in range(len(transacoes_lista)):
  for j in range(len(transacoes_lista[i])):
    transacoes_lista[i][j] = str(transacoes_lista[i][j])
transacoes_lista

"""*Trasnformado em lista, agora o objetivo é inserir no algoritmo a priori.*

# 3 - MÁQUINA PREDITIVA
"""

from apyori import apriori
# Definindo suporte, relevância e elevação
rules = apriori(transactions = transacoes_lista, min_support = 0.003, min_cofindence = 0.2, min_lift = 3, min_length = 2, max_length = 2)

# Verificando as saídas da função apriori
results = list(rules)
results

"""*Os resultados ficarem todos dentro e uma lista e de modo confuso, agora organizaremos os resultados dentro de um **Dataframe**. """

def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])

"""**Resultados Não Ordenados**"""

resultsinDataFrame

"""**Resultados Ordenados**"""

resultsinDataFrame.nlargest(n = 10, columns = 'Lift') # organizando por lift

"""# Conclusão:

Esse exemplo pode ser aplicado em diversos tipos de empreendimentos. Apesar de construção básica, o objetivo foi entender a aplicação do** algoritmo apriori**.
"""

#Autor: Jonatas A. Liberato
#Ref: Eduardo Rocha
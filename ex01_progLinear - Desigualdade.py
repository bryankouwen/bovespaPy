# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:00:18 2019

@author: sergio.amonteiro
"""
#------------------------------------------------------------------------------
#minimize 70x_1 + 80x_2 +85x_3
#{ s.a.} x_1 + 4x_2 + 8x_3   >= 4500
#      40x_1 + 30x_2 + 20x_3 <= 36000
#       3x_1 + 2x_2 + 4x_3   >= 2700
#        x >= 0
#------------------------------------------------------------------------------
import numpy as np
np.set_printoptions(suppress=True)
from scipy.optimize import linprog
from numpy.linalg import solve
import bovespaparser.bovespaparser as bvparser
#------------------------------------------------------------------------------
file = raw_input('Insira o caminho completo com arquivo txt com os dados da Bovespa \n')

with open(file, 'rU') as f:
	result = bvparser.parsedata(f)

a = np.array(result)
acao = a[:,0]
abertura = np.around(a[:,2].astype(np.double),2)
mini = np.around(a[:,3].astype(np.double),2)
maxi = np.around(a[:,4].astype(np.double),2)
fechamento = np.around(a[:,5].astype(np.double),2)
vol = np.around(a[:,6].astype(np.double),2)

# ['CSMG3', datetime.datetime(2019, 4, 30, 0, 0), 67.68, 66.77, 69.64, 69.0, 953900]
#
# 'CSMG3' = (nome da ação)
# datetime.datetime(2019, 4, 30, 0, 0) = data em que ocorreu
# 67.68 = (abertura)
# 66.77 = (mínima)
# 69.64 = (maxima)
# 69.0 =  (fechamento)
# 953900 = (volume)

# obtendo a variavel de retorno da açao (abertura - fechamento)
retorno = (fechamento - abertura)/abertura

# obtendo o risco
media = (abertura + fechamento + mini + maxi)/4
Q = (media - abertura)**2 + (media - fechamento)**2 + (media - mini)**2 + (media - maxi)**2
risco = (Q/3)**0.5

#------------------------------------------------------------------------------
def resolverPLDesigualdade(c, A_ub, b_ub):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub,
                  bounds=(0, None))
    return res
#------------------------------------------------------------------------------
def exemplo01():
    A_ub = np.array(media)
    # Restriçoes risco e investir 100%
    b_ub = np.array(risco)
    #aqui vai ficar oque tem de ser maximizado o retorno r1 r2 r3 etc.
    c = np.array(retorno)
    return c, A_ub, b_ub
#------------------------------------------------------------------------------
#Programa Principal
#------------------------------------------------------------------------------
[c, A_ub, b_ub]=exemplo01();#carregar exemplo 01
#------------------------------------------------------------------------------
resultado=resolverPLDesigualdade(c, A_ub, b_ub); #resolver PL
#------------------------------------------------------------------------------
print('Valor otimo:', resultado.fun)
#------------------------------------------------------------------------------
print("Os valores de x sao:");
nelem=len(resultado.x)
for i in range(nelem):
    print("x[",i+1,"]=",resultado.x[i])
#------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
Created on Thu Mai 19  2019

@author: bryan.kouwen@gmail.com
"""
#------------------------------------------------------------------------------
import numpy as np
np.set_printoptions(suppress=True)
from scipy.optimize import linprog
from numpy.linalg import solve
import bovespaparser.bovespaparser as bvparser
import ipdb
#------------------------------------------------------------------------------

with open('./COTAHIST_M042019.TXT', 'rU') as f:
	result = bvparser.parsedata(f)

a = np.array(result)
acao = a[:,0]
abertura = np.around(a[:,2].astype(np.double),2)
mini = np.around(a[:,3].astype(np.double),2)
maxi = np.around(a[:,4].astype(np.double),2)
fechamento = np.around(a[:,5].astype(np.double),2)
vol = np.around(a[:,6].astype(np.double),2)

# obtendo a variavel de retorno da açao (abertura - fechamento)
retorno = (fechamento - abertura)/abertura

# obtendo o risco
media = (abertura + fechamento + mini + maxi)/4
Q = ((media - abertura)**2 + (media - fechamento)**2 + (media - mini)**2 + (media - maxi)**2)/media
desvio = (Q/4)**0.5
Q= np.around(Q.astype(np.double),2)

def resolverPLDesigualdade(c, A_ub, b_ub):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub,
                  bounds=(0, None))
    return res
#------------------------------------------------------------------------------
def exemplo01():
    A_ub = np.array([desvio])
    b_ub = np.array([0.3])
    c = np.array([retorno])
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
    if not resultado.x[i] <= 0.1:
    	print("x[",i+1,"]=",resultado.x[i], a[i][0])
#------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
Created on Thu Mai 04 2019

@author: bryan.kouwen
"""
#------------------------------------------------------------------------------
#minimize 70x_1 + 80x_2 +85x_3
#{ s.a.} x_1 + x_2 + x_3      = 999
#        x_1 + 4x_2 + 8x_3   <= 4500
#      40x_1 + 30x_2 + 20x_3 <= 36000
#       3x_1 + 2x_2 + 4x_3   <= 2700
#        x >= 0
#------------------------------------------------------------------------------
import numpy as np
import bovespaparser.bovespaparser as bvparser
from scipy.optimize import linprog
from numpy.linalg import solve
#------------------------------------------------------------------------------

with open('filename', 'rU') as f:
	result = bvparser.parsedata(f)

a = np.array(result)
acao = a[:,0]
abertura = a[:,2]
min = a[:,3]
max = a[:,4]
fechamento = a[:,5]
vol = a[:,6] 
#
#
# ['CSMG3', datetime.datetime(2019, 4, 30, 0, 0), 67.68, 66.77, 69.64, 69.0, 953900]
#
# 'CSMG3' = (nome da ação)
# datetime.datetime(2019, 4, 30, 0, 0) = data em que ocorreu
# 67.68 = (abertura)
# 66.77 = (mínima)
# 69.64 = (maxima)
# 69.0 =  (fechamento)
# 953900 = (volume)



#------------------------------------------------------------------------------
def resolverPL(c, A_eq, b_eq, A_ub, b_ub):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                  bounds=(0, None))
    return res
#------------------------------------------------------------------------------
def exemplo01():
    A_eq = np.array([[1,1,1]])
    b_eq = np.array([999])
    A_ub = np.array([[1, 4, 8],
                     [40,30,20],
                     [3,2,4]])
    b_ub = np.array([4500, 36000,2700])
    c = np.array([70, 80, 85])
    return c, A_eq, b_eq, A_ub, b_ub
#------------------------------------------------------------------------------
#Programa Principal
#------------------------------------------------------------------------------
[c, A_eq, b_eq, A_ub, b_ub]=exemplo01();#carregar exemplo 01
#------------------------------------------------------------------------------
resultado=resolverPL(c, A_eq, b_eq, A_ub, b_ub); #resolver PL
#------------------------------------------------------------------------------
print('Valor otimo:', resultado.fun)
#------------------------------------------------------------------------------
print("Os valores de x sao:");
nelem=len(resultado.x)
for i in range(nelem):
    print("x[",i+1,"]=",resultado.x[i])
#------------------------------------------------------------------------------

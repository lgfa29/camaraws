#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Verifica a diferença entre os partidos 
# baseado nas proposições votadas em 2011
# utilizando PCA (análise de componentes primários)

import partidos2
import sys

partidos = []
vetores = []

# recuperação dos vetores de votações
name = 'resultados/vetores.txt'
vfile = open(name, 'r')
flag = 1
for line in vfile:
  if flag % 2 == 1:
    partidos.append(line.rstrip())
  else:
    vetores.append(eval(line))
  flag += 1

# análise das semelhanças
print('Análise PCA')
p = partidos2.semelhanca_pca(vetores)
pc = p.pc()

# impressão
print "Fração da variância explicada pelas dimensões:"
for i in range(0, 4):
  print "%f " % ( p.eigen[i] / p.eigen.sum() )

print "\nCoordenadas:"
for i in range(0,len(partidos)):
  print "%s: [%f, %f]" % (partidos[i], pc[i][0], pc[i][1])

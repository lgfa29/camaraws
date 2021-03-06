# -*- coding: utf-8 -*-
# Classes do modelo de negócio, no caso o XML da proposição
import xml.etree.ElementTree as etree
import io

SIM = 'Sim'
NAO = 'Não'
ABSTENCAO = 'Abstenção'
OBSTRUCAO = 'Obstrução' # por hora será inObstruçãoterpretado como 'Não'

class Proposicao:

  def __init__(self):
    self.id = ''
    self.sigla = ''
    self.numero = ''
    self.ano = ''
    self.ementa = ''
    self.explicacao = ''
    self.situacao = ''
    self.votacoes = []
  
  def fromxml(xml):
    tree = etree.parse(io.StringIO(xml))
    prop = Proposicao()
    prop.sigla = tree.find('Sigla').text
    prop.numero = tree.find('Numero').text
    prop.ano = tree.find('Ano').text
    for child in tree.find('Votacoes'):
      vot = Votacao.fromtree(child)
      prop.votacoes.append(vot)
    return prop

  def __str__(self):
    return "[%s %s/%s]: %s \nEmenta: %s \nSituação: %s" % (self.sigla, self.numero, self.ano, self.explicacao, self.ementa, self.situacao)

class Votacao:

  def __init__(self): 
    self.resumo = ''
    self.data = ''
    self.hora = ''
    self.deputados = []

  def fromtree(tree):
    vot = Votacao() 
    vot.resumo = tree.attrib['Resumo']
    vot.data = tree.attrib['Data']
    vot.hora = tree.attrib['Hora']
    for child in tree:
      dep = Deputado.fromtree(child)
      vot.deputados.append(dep)
    return vot

  def por_partido(self):
    # partido => VotoPartido
    dic = {}
    for dep in self.deputados:
      part = dep.partido
      if not part in dic:
        dic[part] = VotoPartido(part)
      voto = dic[part]
      voto.add(dep.voto)
    return dic  
  
  def por_uf(self):
    # uf => VotoUF
    dic = {}
    for dep in self.deputados:
      uf = dep.uf
      if not uf in dic:
        dic[uf] = VotoUF(uf)
      voto = dic[uf]
      voto.add(dep.voto)
    return dic  

  def __str__(self):
    return "[%s, %s] %s" % (self.data, self.hora, self.resumo)

class Deputado:

  def __init__(self):
    self.nome = ''
    self.partido = ''
    self.uf = ''
    self.voto = ''

  def fromtree(tree):
    dep = Deputado()
    dep.nome = tree.attrib['Nome']
    dep.partido = tree.attrib['Partido']
    dep.uf = tree.attrib['UF']
    dep.voto = tree.attrib['Voto']
    return dep

  def __str__(self):
    return "%s (%s-%s) votou %s" % (self.nome, self.partido, self.uf, self.voto)
  
class Voto:

  def add(self, voto):
    if (voto == SIM):
      self.sim += 1
    if (voto == NAO):
      self.nao += 1
    if (voto == OBSTRUCAO): # pode ser mudado no futuro
      self.nao += 1
    if (voto == ABSTENCAO):
      self.abstencao += 1

  def __init__(self):
    self.sim = 0
    self.nao = 0
    self.abstencao = 0

  def __str__(self):
    return '(%s, %s, %s)' % (self.sim, self.nao, self.abstencao)

class VotoPartido(Voto):

  def __init__(self, partido):
    Voto.__init__(self)
    self.partido = partido

class VotoUF(Voto):

  def __init__(self, uf):
    Voto.__init__(self)
    self.uf = uf



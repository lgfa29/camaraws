import algebra

def vetor_votacoes(partido, proposicoes):
  vetor = []
  for prop in proposicoes:
    for votacao in prop.votacoes:
      dic = votacao.por_partido()
      voto = dic[partido]
      #vi = (voto.sim + 0.5*voto.abstencao) / (voto.sim + voto.nao + voto.abstencao) # análise antigo
      vi = (1*voto.sim + 0*voto.abstencao -1*voto.nao) / (voto.sim + voto.nao + voto.abstencao)
      vetor.append(vi)
  return vetor  

def semelhanca_vetores(vetor1, vetor2):
  nv1 = algebra.normaliza(vetor1)
  nv2 = algebra.normaliza(vetor2)
  return algebra.prod_escalar(nv1, nv2)

def semelhanca(partido1, partido2, proposicoes):
  v1 = vetor_votacoes(partido1, proposicoes)
  v2 = vetor_votacoes(partido2, proposicoes)
  sem = semelhanca_vetores(v1, v2)
  return (sem+1)/2



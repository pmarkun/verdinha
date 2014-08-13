# Script para importar os arquivos de candidatos 2014.

import csvkit, json

lista = []
ufs = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO","BR"]

for uf in ufs:
	print 'Getting '+uf
	cand = open("../raw/consulta_cand_2014_"+UF+".txt", 'r')
	cand = csvkit.reader(cand, encoding='iso-8859-1', delimiter=';')
	for c in cand:
		#if c[15] == 'DEFERIDO': #muitas candidaturas ainda nao foram deferidas
		lista.append(c[10])
		if c[9] in ['GOVERNADOR', 'PRESIDENTE']: #adiciona tambem o nome de urna nesses casos
			lista.append(c[13])

with open('cand.json', 'w') as final:
	final.write(json.dumps(lista))
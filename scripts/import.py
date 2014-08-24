# -*- coding: utf-8 -*- 
# Script para importar os arquivos de candidatos 2014, doacoes 2010 e 2014.
# TODO: Importar congressistas!

import csvkit, json, os

estados = {
	"DISTRITO FEDERAL" : "DF",
	"RORAIMA" : "RR",
	"ACRE" : "AC",
	u'S\xc3O PAULO' : "SP",
	u'CEAR\xc1' : "CE",
	u'ESP\xcdRITO SANTO' : "ES",
	u'ROND\xd4NIA' : "RO",
	u'RIO DE JANEIRO' : "RJ",
	u'PARAN\xc1' : "SC",
	u'BAHIA' : "BA",
	u'RIO GRANDE DO SUL' : "RS",
	u'MINAS GERAIS' : "MG",
	u'GOI\xc1S' : "GO",
	u'PAR\xc1' : "PA",
	u'MATO GROSSO DO SUL' : "MS",
	"MATO GROSSO" : "MT",
	"SANTA CATARINA" : "SC",
	"ALAGOAS" : "AL",
	u'TOCANTINS' : "TO",
	u'AMAP\xc1' : "AP",
	"AMAZONAS" : "AM",
	u'PERNAMBUCO' : "PE",
	u'PIAU\xcd' : "PI",
	u'RIO GRANDE DO NORTE' : "RN",
	u'PARA\xcdBA' : "PB",
	u'SERGIPE' : "SE",
	u'MARANH\xc3O' : "MA",
	"BRASIL" : "BR"

}

def mongo_save(itens, colecao, clear=False):
	'''Salva um dicionario no mongo
	'''
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db[colecao]
	if (clear):
		print "Dropping..."
		col.drop()
	print "Saving..."
	for i in itens:
		col.update({'_id' : i}, itens[i], upsert=True)

def importaCandidatos(arquivo):
	raw = open(arquivo, 'r')
	raw = csvkit.reader(raw, encoding='iso-8859-1', delimiter=';')
	candidatos = {}
	for c in raw:
		candidatos[c[26]] = {
			'nome' : c[10],
			'apelidos' : [c[13]],
			'_id' : c[26],
			'candidaturas' : {}
		}
	mongo_save(candidatos, 'politicos', True)

def importaPrestacoes2010(arquivo):
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db.politicos
	
	presentes = []
	ausentes = []
	raw = open(arquivo, 'r')
	doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
	for d in doacoes_raw:
		if d['Nome candidato'] not in presentes and d['Nome candidato'] not in ausentes:
			p = col.find_one({'nome' : d['Nome candidato']})
			if p:
				presentes.append(d['Nome candidato'])
			else:
				ausentes.append(d['Nome candidato']) #hackish sleepy
		if d['Nome candidato'] in presentes:
			if not p['candidaturas'].has_key('2010'):
				p['candidaturas']['2010'] = {
							'ano' : 2010,
							'cargo' : d['Cargo'],
							'situacao' : '',
							'numero' : d[u'Número candidato'],
							'partido' : d['Sigla Partido'],
							'uf' : d['UF'],
							'doacoes' : {},
							'total' : 0
						}
				
			p['candidaturas']['2010']['total'] += float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
			cnpj_id = d['CPF/CNPJ do doador'].replace('/','').replace('-','').replace('.','')
			if not p['candidaturas']['2010']['doacoes'].has_key(cnpj_id):	
				p['candidaturas']['2010']['doacoes'][cnpj_id] = {
					'nome' : d['Nome do doador'],
					'cnpj' : d['CPF/CNPJ do doador'],
					'valor' : float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
				}
				#todo doador originario
			else:
				p['candidaturas']['2010']['doacoes'][cnpj_id]['valor'] += float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
			col.update({'_id' : p['_id']}, p, upsert=True)

def processaPrestacoes2010():
	for folder,z,c in os.walk('../raw/prestacao2010/candidato'):
		arquivo = folder + '/ReceitasCandidatos.txt'
		if os.path.isfile(arquivo):
			print 'Getting ' + arquivo
			importaPrestacoes2010(arquivo)

def importaPrestacoes2014(arquivo, mugshot):
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db.politicos
	
	raw = open(arquivo, 'r')
	doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
	c = doacoes_raw.next()
	p = col.find_one({'nome' : c['Nome do Candidato']})
	if not p:
		print c['Nome do Candidato'] + " not found..."
		print arquivo
	else:
		raw.seek(0) #rewind!
		doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
		for d in doacoes_raw:
			p['mugshot'] = mugshot
			if not p['candidaturas'].has_key('2014'):
				p['candidaturas']['2014'] = {
							'ano' : 2014,
							'cargo' : d['Candidatura'],
							'situacao' : 'Candidato',
							'numero' : d[u'Número do Candidato'],
							'partido' : d['Partido'],
							'uf' : estados[d['Unidade Eleitoral']],
							'doacoes' : {},
							'total' : 0
						}
				
			p['candidaturas']['2014']['total'] += float(d['Valor R$'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
			cnpj_id = d['CPF/CNPJ'].replace('/','').replace('-','').replace('.','')
			if not p['candidaturas']['2014']['doacoes'].has_key(cnpj_id):	
				p['candidaturas']['2014']['doacoes'][cnpj_id] = {
					'nome' : d['Doador'],
					'cnpj' : d['CPF/CNPJ'],
					'valor' : float(d['Valor R$'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
				}
				#todo doador originario
			else:
				p['candidaturas']['2014']['doacoes'][cnpj_id]['valor'] += float(d['Valor R$'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
			col.update({'_id' : p['_id']}, p, upsert=True)

def processaPrestacoes2014():
	print "Processando..."
	for arquivo in os.listdir('../raw/prestacao2014/candidatos'):
		p = '../raw/prestacao2014/candidatos/'+arquivo
		if os.path.isfile(p) and os.path.getsize(p) > 0:
			importaPrestacoes2014(p, arquivo[:-4])

#importaCandidatos('../raw/candidaturas2014/candidatos_total.csv')

# -*- coding: utf-8 -*- 
# Script para importar os arquivos de candidatos 2014, doacoes 2010 e 2014.
# TODO: Importar congressistas!

import csvkit, json, os, unidecode

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
	print "Importando candidatos"
	raw = open(arquivo, 'r')
	raw = csvkit.reader(raw, encoding='iso-8859-1', delimiter=';')
	candidatos = {}
	lista = {}
	for c in raw:
		c[10] = unidecode.unidecode(c[10])
		if c[9] in ['GOVERNADOR', 'PRESIDENTE', 'DEPUTADO FEDERAL', 'SENADOR']:
			candidatos[c[26]] = {
				'nome' : c[10],
				'apelidos' : [c[13]],
				'_id' : c[26],
				'candidaturas' : {},
				'mugshot' : c[11]
			}
			candidatos[c[26]]['candidaturas']['2014'] = {
				'cargo' : c[9],
				'situacao' : c[15],
				'numero' : c[12],
				'partido' : c[17],
				'uf' : c[5],
				'doacoes' : {},
				'total' : 0,
			}

		# Salva lista
		if c[9] not in ['REMOVER']:
				lista[c[10]] = 0
		if c[9] in ['GOVERNADOR', 'PRESIDENTE']: #adiciona tambem o nome de urna nesses casos
				lista[c[13]] = c[10]
	mongo_save(candidatos, 'politicos', True)
	with open('names.js', 'w') as final:
		header ="var nick = "
		final.write(header+json.dumps(lista))

def preImportaPrestacoes2010(arquivo):
	candidatos = {}
	raw = open(arquivo, 'r')
	doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
	for d in doacoes_raw:
		d['Nome candidato'] = unidecode.unidecode(d['Nome candidato'])
		if not candidatos.has_key(d['Nome candidato']):
			candidatos[d['Nome candidato']] = {
				'ano' : 2010,
				'cargo' : d['Cargo'],
				'situacao' : '',
				'numero' : d[u'Número candidato'],
				'partido' : d['Sigla Partido'],
				'uf' : d['UF'],
				'doacoes' : {},
				'total' : 0
			}
		else:
			candidatos[d['Nome candidato']]['total'] += float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
			cnpj_id = d['CPF/CNPJ do doador'].replace('/','').replace('-','').replace('.','')
			if not candidatos[d['Nome candidato']]['doacoes'].has_key(cnpj_id):	
				candidatos[d['Nome candidato']]['doacoes'][cnpj_id] = {
					'nome' : d['Nome do doador'],
					'cnpj' : d['CPF/CNPJ do doador'],
					'valor' : float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
				}
				#todo doador originario
			else:
				candidatos[d['Nome candidato']]['doacoes'][cnpj_id]['valor'] += float(d['Valor receita'].strip('R$ ').strip('\.').replace('.','').replace(',','.'))
	importaPrestacoes2010(candidatos)

def importaPrestacoes2010(candidatos):
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db.politicos
	
	for d in candidatos:
		p = col.find_one({'nome' : d})
		if p:
			p['candidaturas']['2010'] = candidatos[d]
			col.update({'_id' : p['_id']}, p, upsert=True)

def processaPrestacoes2010():
	print "Processando 2010..."
	for folder,z,c in os.walk('../raw/prestacao2010/candidato'):
		arquivo = folder + '/ReceitasCandidatos.txt'
		if os.path.isfile(arquivo):
			print 'Getting ' + arquivo
			preImportaPrestacoes2010(arquivo)

def importaPrestacoes2014(arquivo, mugshot):
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db.politicos
	
	raw = open(arquivo, 'r')
	doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
	c = doacoes_raw.next()
	if c.has_key('prestacao'):
		#print arquivo + " nao entregue"
		return None
	c['Nome do Candidato'] = unidecode.unidecode(c['Nome do Candidato'])
	p = col.find_one({'nome' : c['Nome do Candidato']})
	if p:
		raw.seek(0) #rewind!
		doacoes_raw = csvkit.DictReader(raw, encoding='iso-8859-1', delimiter=';')
		for d in doacoes_raw:
			#p['mugshot'] = mugshot
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
	print "Processando 2014..."
	for arquivo in os.listdir('../raw/prestacao2014/candidatos'):
		p = '../raw/prestacao2014/candidatos/'+arquivo
		if os.path.isfile(p) and os.path.getsize(p) > 0:
			try:
				importaPrestacoes2014(p, arquivo[:-4])
			except:
				print arquivo

importaCandidatos('../raw/candidaturas2014/candidatos_total.csv')
processaPrestacoes2014()
processaPrestacoes2010()

# -*- coding: utf-8 -*- 
# Script para importar os arquivos de candidatos 2014.

import csvkit, json, os
from lxml.etree import parse
import urllib2, unidecode

def generateTSECand():
	'''Gera names.json a partir dos arquivos de candidatura de 2014 na pasta.
	   http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2014.zip
	'''
	lista = {}
	ufs = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO","BR"]
	for uf in ufs:
		print 'Getting '+uf
		cand = open("../raw/candidaturas2014/consulta_cand_2014_"+uf+".txt", 'r')
		cand = csvkit.reader(cand, encoding='iso-8859-1', delimiter=';')
		for c in cand:
			#if c[15] == 'DEFERIDO': #muitas candidaturas ainda nao foram deferidas
			#if c[9] not in ['REMOVER']:
			#	lista[unidecode.unidecode(c[10])] = 0
			if c[9] in ['GOVERNADOR', 'PRESIDENTE']: #adiciona tambem o nome de urna nesses casos
				lista[unidecode.unidecode(c[10])] = 0
				lista[c[13]] = unidecode.unidecode(c[10])
	return lista

def createNames():
	lista = {}
	nomesTSE = generateTSECand()
	nomesCamara = generateCamaraNomeParlamentar()
	nomesSenado = generateSenadoNomeParlamentar()
	
	lista.update(nomesTSE)
	lista.update(nomesCamara)
	lista.update(nomesSenado)		
			

	with open('names.js', 'w') as final:
		header ="var nick = "
		final.write(header+json.dumps(lista))


def mongo_save(itens, clear=False):
	'''Salva um dicionario no mongo
	'''
	from pymongo import MongoClient
	client = MongoClient()
	db = client.verdinha
	col = db.doacoes
	if (clear):
	    col.drop()
	for i in itens:
	    col.update({'_id' : i}, itens[i], upsert=True)

def generateDoacao(arquivo):
	'''Utiliza os arquivos ReceitaCand.txt das Prestações de Contas de 2010
	   http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_contas_2010.zip
	'''
	doacoes_raw = open(arquivo, 'r')
	doacoes_raw = csvkit.DictReader(doacoes_raw, encoding='iso-8859-1', delimiter=';')

	r = {}
	for d in doacoes_raw:
		_id = d['CPF do candidato']
		if not r.has_key(_id):
			r[_id] = {
				'_id' : _id,
				'nome' : d['Nome candidato'],
				'numero' : d[u'Número candidato'],
				'partido' : d['Sigla Partido'],
				'uf' : d['UF'],
				'doacoes' : {},
				'total' : 0
			}
		
		r[_id]['total'] += float(d['Valor receita'].replace(',','.'))
		if not r[_id]['doacoes'].has_key(d['CPF/CNPJ do doador']):	
			r[_id]['doacoes'][d['CPF/CNPJ do doador']] = {
				'nome' : d['Nome do doador'],
				'valor' : float(d['Valor receita'].replace(',','.'))
			}
		else:
			r[_id]['doacoes'][d['CPF/CNPJ do doador']]['valor'] += float(d['Valor receita'].replace(',','.'))

	print 'Saving...'
	mongo_save(r)

def generateDoacoes():
	for folder,z,c in os.walk('../raw/prestacao2010/candidato'):
		arquivo = folder + '/ReceitasCandidatos.txt'
		if os.path.isfile(arquivo):
			print 'Getting ' + folder.split('/')[-1]
			generateDoacao(arquivo)



def generateCamaraNomeParlamentar():
	'''Gera nomes parlamentares para o nomes.js a partir dos dados do XML da Câmara'''
	soup = parse(urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados"))
	deputados = {}
	for d in soup.xpath("//deputado"):
		nome_completo = unidecode.unidecode(unicode(d.xpath('nome')[0].text))
		nome_parlamentar = d.xpath('nomeParlamentar')[0].text
		deputados[nome_completo] = 0
		deputados[nome_parlamentar] = nome_completo
	return deputados

def generateSenadoNomeParlamentar():
	'''Gera nomes parlamentares para o nomes.js a partir dos dados do XML da Câmara'''
	soup = parse(urllib2.urlopen("http://legis.senado.leg.br/dadosabertos/senador/lista/atual"))
	senadores = {}
	for d in soup.xpath("//Parlamentar/IdentificacaoParlamentar"):
		nome_completo = unidecode.unidecode(unicode(d.xpath('NomeCompletoParlamentar')[0].text)).upper()
		nome_parlamentar = d.xpath('NomeParlamentar')[0].text.upper()
		senadores[nome_completo] = 0
		senadores[nome_parlamentar] = nome_completo
	return senadores
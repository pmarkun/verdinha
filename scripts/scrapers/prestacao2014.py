import sys
from lxml.etree import parse as parsexml
from lxml.html import parse
import json, urllib2, os, time, socket

diretorio = sys.argv[1]

def getCandidatos():
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/candidatoAutoComplete.do?noCandLimpo=&orderBy=cand.NM_CANDIDATO"
	candidatos = []
	estados = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO","BR"]

	codigos = {"Presidente" : 1,"Vice-Presidente" : 2,"Governador" : 3,"Vice-Governador" : 4,"Senador" : 5,"1o Suplente Senador" : 9,"2o Suplente Senador" : 10,"Deputado Federal" : 6,"Deputado Estadual" : 7,"Deputado Distrital" : 8}

	errors = []
	for UF in estados:
		for COD in codigos:
			print "Getting " + UF + " " + COD		
			try:
				site = parsexml(base_url+"&sgUe="+UF+"&cdCargo="+str(codigos[COD])).getroot()
				candidatos += raspa(site)
			except:
				print "Error getting " + UF + " " + COD
				errors.append("Error getting " + UF + " " + COD)

	arquivo = open(diretorio+'/candidatos2014.json', 'w')
	arquivo.write(json.dumps(candidatos, indent=4))
	arquivo.close()

def raspaCandidato(site):
	cand = []
	for index, link in enumerate(site.xpath('//sqCand')):
		c = link.text
		com = {
			'id' : c,
			'nome': site.xpath('//name')[index].text.strip(),
			'uf': site.xpath('//sgUe')[index].text.strip(),
			'numero': site.xpath('//numero')[index].text.strip(),
			'partido': site.xpath('//partido')[index].text.strip(),
			'cargo': COD
		}
		if (com['id'] != '.'):
			cand.append(com)
	return cand


def getComites():
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/listaComiteDirecaoPartidaria.action?nrPartido=&municipio=&siglaUf="
	comites = []
	estados = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO","BR"]

	for UF in estados:
		print "Getting " + UF
		site = parse(base_url+UF).getroot()
		for link in site.xpath('//a'):
			c = link.get('href').split("'")
			com = {
				'id' : c[1],
				'nome': c[3],
				'partido': c[5],
				'uf': c[7],
				'pais': c[9]
			}
			comites.append(com)

	arquivo = open(diretorio+'comites.json', 'w')
	arquivo.write(json.dumps(comites, indent=4))
	arquivo.close()

def prestacao_candidatos():
	candidatos = json.load(open(diretorio+'/candidatos.json'))
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/resumoReceitasByCandidato.action"
	base_post = "sgUe=&rb1=on&rbTipo=on&tipoEntrega=1&nrCandidato=&nmCandidato=&sgUfMunicipio=&sgPartido=&nomeDoador=&cpfCnpjDoador=&action%3AexportaReceitaCsvCandidato=Exportar+como+planilha&sqCandidato="
	wait_period = 1
	counter = 0
	for c in candidatos:
		if not os.path.isfile(diretorio+'/candidatos/'+c['id']+'.csv'):
			if counter > 50:
				print "Respira fundo!"
				time.sleep(wait_period*3)
				counter = 0
			counter += 1
			_id = c['id']
			print 'Getting ' + str(_id)
			try:
				planilha = urllib2.urlopen(base_url, data=base_post+_id, timeout=10)
				with open(diretorio+'/candidatos/'+_id+'.csv', 'w') as arquivo:
					arquivo.write(planilha.read())
			except socket.timeout:
				print "Ugga! Respira mais!"
				time.sleep(wait_period*5)
				prestacao_candidatos()

def prestacao_comites():
	comites = json.load(open(diretorio+'/comites.json'))
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/resumoReceitasByComite.action"
	base_post = "sgUe=&rb1=on&rbTipo=on&tipoEntrega=1&nomeOrgao=&sgUfMunicipio=&sgPartido=&nomeDoador=&cpfCnpjDoador=&action%3AexportaReceitaCsvComite=Exportar+como+Planilha&sqComiteFinanceiro="
	wait_period = 1
	counter = 0
	for c in comites:
		if not os.path.isfile(diretorio+'/comites/'+c['id']+'.csv'):
			if counter > 50:
				print "Respira fundo!"
				time.sleep(wait_period*3)
				counter = 0
			counter += 1
			_id = c['id']
			print 'Getting' + str(_id)
			try:
				planilha = urllib2.urlopen(base_url, data=base_post+_id, timeout=10)
				with open(diretorio+'/comites/'+_id+'.csv', 'w') as arquivo:
					arquivo.write(planilha.read())
			except socket.timeout:
				print "Ugga! Respira mais!"
				time.sleep(wait_period*5)
				prestacao_comites()


# Baixa comites 2014
if not os.path.isfile(diretorio+'/comites.json'):
	print "Listando comites..."
	getComites()

# Baixa candidatos 2014
if not os.path.isfile(diretorio+'/candidatos.json'):
	print "Listando candidatos..."
	getCandidatos()

# Baixa prestacao 2014
if os.path.isfile(diretorio+'/comites.json'):
	print "Baixando comites..."
	prestacao_comites()
if os.path.isfile(diretorio+'/candidatos.json'):
	print "Baixando candidatos..."
	prestacao_candidatos()
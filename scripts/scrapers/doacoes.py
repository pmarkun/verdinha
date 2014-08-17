import json, urllib2, os, time, socket

candidatos = json.load(open('candidatos.json'))
def roda(candidatos):
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/resumoReceitasByCandidato.action"
	base_post = "sgUe=&rb1=on&rbTipo=on&tipoEntrega=1&nrCandidato=&nmCandidato=&sgUfMunicipio=&sgPartido=&nomeDoador=&cpfCnpjDoador=&action%3AexportaReceitaCsvCandidato=Exportar+como+planilha&sqCandidato="
	wait_period = 1
	counter = 0
	for c in candidatos:
		if not os.path.isfile('../../raw/prestacao2014/'+c['id']+'.csv'):
			if counter > 50:
				print "Respira fundo!"
				time.sleep(wait_period*3)
				counter = 0
			counter += 1
			_id = c['id']
			print 'Getting' + str(_id)
			try:
				planilha = urllib2.urlopen(base_url, data=base_post+_id, timeout=10)
				with open('../../raw/prestacao2014/'+_id+'.csv', 'w') as arquivo:
					arquivo.write(planilha.read())
			except socket.timeout:
				print "Ugga! Respira mais!"
				time.sleep(wait_period*5)
				roda(candidatos)
		

roda(candidatos)
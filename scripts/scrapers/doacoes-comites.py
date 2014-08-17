import json, urllib2, os, time, socket

comites = json.load(open('comites.json'))
def roda(comites):
	base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/resumoReceitasByComite.action"
	base_post = "sgUe=&rb1=on&rbTipo=on&tipoEntrega=1&nomeOrgao=&sgUfMunicipio=&sgPartido=&nomeDoador=&cpfCnpjDoador=&action%3AexportaReceitaCsvComite=Exportar+como+Planilha&sqComiteFinanceiro="
	wait_period = 1
	counter = 0
	for c in comites:
		if not os.path.isfile('../../raw/prestacao2014/comites/'+c['id']+'.csv'):
			if counter > 50:
				print "Respira fundo!"
				time.sleep(wait_period*3)
				counter = 0
			counter += 1
			_id = c['id']
			print 'Getting' + str(_id)
			try:
				planilha = urllib2.urlopen(base_url, data=base_post+_id, timeout=10)
				with open('../../raw/prestacao2014/comites/'+_id+'.csv', 'w') as arquivo:
					arquivo.write(planilha.read())
			except socket.timeout:
				print "Ugga! Respira mais!"
				time.sleep(wait_period*5)
				roda(comites)
		

roda(comites)
from lxml.etree import parse
import json

def raspa(site):
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

base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/candidatoAutoComplete.do?noCandLimpo=&orderBy=cand.NM_CANDIDATO"
candidatos = []
estados = ["AC", "AL", "AM", "AP",  "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO","BR"]

codigos = {"Presidente" : 1,"Vice-Presidente" : 2,"Governador" : 3,"Vice-Governador" : 4,"Senador" : 5,"1o Suplente Senador" : 9,"2o Suplente Senador" : 10,"Deputado Federal" : 6,"Deputado Estadual" : 7,"Deputado Distrital" : 8}

errors = []
for UF in estados:
	for COD in codigos:
		print "Getting " + UF + " " + COD		
		try:
			site = parse(base_url+"&sgUe="+UF+"&cdCargo="+str(codigos[COD])).getroot()
			candidatos += raspa(site)
		except:
			print "Error getting " + UF + " " + COD
			errors.append("Error getting " + UF + " " + COD)

arquivo = open('candidatos.json', 'w')
arquivo.write(json.dumps(candidatos, indent=4))
arquivo.close()
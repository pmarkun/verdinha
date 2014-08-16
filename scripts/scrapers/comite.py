from lxml.html import parse
import json

base_url = "http://inter01.tse.jus.br/spceweb.consulta.receitasdespesas2014/listaComiteDirecaoPartidaria.action?nrPartido=&municipio=&siglaUf="
comites = []
estados = ['BR']

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

arquivo = open('comites.json', 'w')
arquivo.write(json.dumps(comites, indent=4))
arquivo.close()
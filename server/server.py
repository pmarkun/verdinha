from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify, cifras
from flask.ext.pymongo import PyMongo
from settings import *
import operator

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'verdinha'
app.config['MONGO_USERNAME'] = SETTINGS['username']
app.config['MONGO_PASSWORD'] = SETTINGS['password']
mongo = PyMongo(app)
app.jinja_env.filters['cifras'] = cifras

#tmp
@app.route("/")
def index():
	return redirect("http://www.verdinhas.org.br/website", code=302)

@app.route("/busca/<nome>")
@app.route("/busca/<nome>/<ext>")
def busca(nome, ext='html'):
	resultado = mongo.db.politicos.find_one({"nome": nome})
	if resultado:
		if ext == 'json':
			return jsonify(resultado)
		else:
			if not resultado['candidaturas'].has_key('2010'):
				resultado['candidaturas']['2010'] = {
					'total' : 0,
					'outras_doacoes' : 0.0
				}
			else:
				resultado['candidaturas']['2010']['doacoes'] = sorted(resultado['candidaturas']['2010']['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
				resultado['candidaturas']['2010']['outras_doacoes'] = float(resultado['candidaturas']['2010']['total'])
				for r in resultado['candidaturas']['2010']['doacoes']:
					resultado['candidaturas']['2010']['outras_doacoes'] += -1*float(r[1]['valor'])

			if not resultado['candidaturas'].has_key('2014'):
				resultado['candidaturas']['2014'] = {
					'total' : 0,
					'outras_doacoes' : 0.0
				}
			else:
				resultado['candidaturas']['2014']['doacoes'] = sorted(resultado['candidaturas']['2014']['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
				resultado['candidaturas']['2014']['outras_doacoes'] = float(resultado['candidaturas']['2014']['total'])
				for r in resultado['candidaturas']['2014']['doacoes']:
					resultado['candidaturas']['2014']['outras_doacoes'] += -1*float(r[1]['valor'])
			return render_template('popup.html', data=resultado)
	else:
		abort(404)

@app.route("/cnpj/<cnpj>")
def cnpj(cnpj):
	resultado = {
		'nome' : '',
		'candidaturas' : {
			'2014' : {
				'doacoes' : {},
				'total' : 0,
				'outras_doacoes' : 0.0
			},
			'2010' : {
				'doacoes' : {},
				'total' : 0,
				'outras_doacoes' : 0
			}
		}
	}

	#hackish slugish
	for ano in ['2010','2014']:
		query = {"candidaturas."+ano+".doacoes."+cnpj : { "$exists" : "true"}}
		#fields = ["candidaturas.2014.doacoes."+cnpj]
		sort = [("candidaturas."+ano+".doacoes."+cnpj+".valor", 'DESCENDING')]
		result = mongo.db.politicos.find(query)
		for i in result:
			resultado['nome'] = i['candidaturas'][ano]['doacoes'][cnpj]['nome']
			resultado['candidaturas'][ano]['doacoes'][i['nome']] = {
				'nome' : i['nome'] + " " + i['candidaturas'][ano]['partido']+"/"+i['candidaturas'][ano]['uf'],
				'valor' : i['candidaturas'][ano]['doacoes'][cnpj]['valor']
			}
		
		for r in resultado['candidaturas'][ano]['doacoes']:
			resultado['candidaturas'][ano]['total'] += resultado['candidaturas'][ano]['doacoes'][r]['valor']
		resultado['candidaturas'][ano]['doacoes'] = sorted(resultado['candidaturas'][ano]['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
		resultado['candidaturas'][ano]['outras_doacoes'] = float(resultado['candidaturas'][ano]['total'])
		for r in resultado['candidaturas'][ano]['doacoes']:
			resultado['candidaturas'][ano]['outras_doacoes'] += -1*float(r[1]['valor'])
	return render_template('popup.html', data=resultado)


if __name__ == "__main__":
	app.run(debug=True)
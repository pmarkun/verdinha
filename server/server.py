from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify
from flask.ext.pymongo import PyMongo
import operator

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'verdinha'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
mongo = PyMongo(app)

#tmp
@app.route("/")
def index():
	return render_template('front.html')

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
					'total' : 0
				}
			else:
				resultado['candidaturas']['2010']['doacoes'] = sorted(resultado['candidaturas']['2010']['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
			if not resultado['candidaturas'].has_key('2014'):
				resultado['candidaturas']['2014'] = {
					'total' : 0
				}
			else:
				resultado['candidaturas']['2014']['doacoes'] = sorted(resultado['candidaturas']['2014']['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
			return render_template('popup.html', data=resultado)
	else:
		abort(404)

if __name__ == "__main__":
	app.run(debug=True)
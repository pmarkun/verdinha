from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify
from flask.ext.pymongo import PyMongo
import operator

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'verdinha'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
mongo = PyMongo(app)

@app.route("/")
def index():
	return render_template('front.html')

@app.route("/busca/<nome>")
@app.route("/busca/<nome>/<ext>")
def busca(nome, ext='html'):
	resultado = mongo.db.doacoes.find_one({"nome": nome})
	if resultado:
		if ext == 'json':
			return jsonify(resultado)
		else:
			resultado['doacoes'] = sorted(resultado['doacoes'].iteritems(), key=lambda x: x[1]['valor'], reverse=True)[0:5]
			return render_template('popup.html', data=resultado)
	else:
		abort(404)

if __name__ == "__main__":
	app.run(debug=True)
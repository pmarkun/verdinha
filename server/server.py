from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'verdinha'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
mongo = PyMongo(app)

@app.route("/")
def index():
	return render_template('front.html')

@app.route("/busca/<nome>")
def busca(nome):
	resultado = mongo.db.doacoes.find_one({"nome": nome})
	if resultado:
		return jsonify(resultado)
	else:
		abort(404)

if __name__ == "__main__":
	app.run(debug=True)
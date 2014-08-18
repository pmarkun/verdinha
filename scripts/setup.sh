# Baixa e processa arquivos do TSE de 2010 e 2014.

# Cria diretorios necessarios
mkdir -p ../raw/tmp
mkdir -p ../raw/candidaturas2014
mkdir -p ../raw/prestacao2010
mkdir -p ../raw/prestacao2014


#Baixa arquivos
if [ ! -f ../raw/tmp/consulta_cand_2014.zip ]; then
    echo "Baixando candidatos 2014"
    wget http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2014.zip -P ../raw/tmp
	unzip ../raw/tmp/consulta_cand_2014.zip -d ../raw/candidaturas2014
fi

#Baixar base de doacoes de 2010
if [ ! -f ../raw/tmp/prestacao_contas_2010.zip ]; then
	echo "Baixando prestacao 2010..."
	wget http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_contas_2010.zip -P ../raw/tmp
	unzip ../raw/tmp/prestacao_contas_2010.zip -d ../raw/prestacao2010
fi

#Baixar base de doacoes de 2014
python scrapers/prestacao2014.py ../raw/prestacao2014
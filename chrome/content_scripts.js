//Captura o innerHTML da página.
var texto = document.body.innerHTML;

//Sobe o texto todo para uppercase (economiza tempo com busca case insensitive.)
texto = texto.toUpperCase();

//Envia mensagem pro background com o texto.
chrome.runtime.sendMessage({greeting: texto}, function(response) {
  //Checa resposta em busca de matches
  if (response.farewell && response.farewell.length > 0) {
  	response.farewell.forEach(function(entry) {
		//Expressão regular para buscar o nome do candidato apenas no texto do html
		//TODO: Filtrar para apenas textos dentro de <p>,<div> e eventualmente <span>.
		var re = new RegExp("(<p.*>|<div.*>)([^<]*)(\b"+entry+"\b)","gi");
		
		//Debug
		console.log(re);
		console.log(re.exec(document.body.innerHTML));
		//Debug end

		//Substitui por um <a> com title dummy.
		//TODO: Substitutir por span com onclick e definir função JS que carrega dados dinamicamente.
		document.body.innerHTML = document.body.innerHTML.replace(re, '$1$2<a href="#" title="MAIORES DOAÇÕES 2010&#013;SUZANO PAPEL E CELULOSE	1046289.43&#013;SUCOCITRICO CUTRALE LTDA	1000000&#013;CONTRUÇÕES E COMERCIO CAMARGO CORREA S/A	600000">$3</a>');
  	});
  }
  
  //Debug
  else {

  	alert("None found.");
  }
  //Debug end
});
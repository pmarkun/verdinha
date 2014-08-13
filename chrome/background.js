//Função para baixar o JSON sincronamente.
function getRemote(remote_url) {
    return $.ajax({
    	dataType: "json",
        type: "GET",
        url: remote_url,
        async: false
    }).responseJSON;
}

//Checa a existencia dos nomes do cand.json
function checaNomes(texto, nomes) {
	matches = [];
	nomes.forEach(function(entry) {
    	match = (new RegExp(entry)).test(texto);
			if (match) {
				matches.push(entry);
			}
		});
	console.log(matches);
	return matches;
}

//Baixa sincronamente o cand.json 
nomes = getRemote(chrome.extension.getURL('/data/cand.json'));


// Listener para quando o usuario clica no botão.
chrome.browserAction.onClicked.addListener(function(tab) {
  console.log('Analisando ' + tab.url + '!');
  //Executa o content_scripts.js na página referida.
  chrome.tabs.executeScript(null, {
  		file: 'content_scripts.js'
	});
});

// Listener para onetime messages.
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    	if (request.greeting) {
    		//Analisa o innerHTML da página
      		matches = checaNomes(request.greeting, nomes);
  			//Envia os nomes encontrados
  			sendResponse({farewell: matches});
  		}
	});
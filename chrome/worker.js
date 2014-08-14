self.onmessage = function(event) {
  var matches = {};
  for (nome in event.data.nomes) {
  	match = (new RegExp(nome)).test(event.data.texto);
  	if (match) {
  		matches[nome] = event.data.nomes[nome];
  	}
  }
  postMessage(matches);
}
// JavaScript Document
function rank(data, count) {
  var sort_array = [];
  for (var key in data.doacoes) {
    sort_array.push({nome:data.doacoes[key].nome, valor:data.doacoes[key].valor});
  }
  // Now sort it:
  sort_array.sort(function(x,y){return x.valor - y.valor});
  var top10 = sort_array.reverse().slice(0,count+1);
  return top10;
}

function checaNomes(texto, nomes) {
  var matches = {};
  $.each(nomes, function (entry, value) {
    match = (new RegExp(entry)).test(texto);
    if (match) {
      matches[entry] = value;
    }
  });
  return matches;
}

function highlight(matches) {
  $.each(matches, function(key, value) {
    var nome_completo = key;
    if (value != 0) {
      nome_completo = value;
    }
    $("p").highlight(key, {caseSensitive: false, className: 'highlight-1337', wordsOnly:true, dataAttr: nome_completo});
  });

  $('.highlight-1337').each(function() {
    var nome = $(this).attr("data-highlight");
    $(this).tooltipster({
      content : 'Loading...',
      functionBefore: function(origin, continueTooltip) {
        continueTooltip();

        $.getJSON("http://127.0.0.1:5000/busca/"+nome, function (data) {
          var top10 = rank(data, 5);
          var dummy = $("<div/>")
          dummy.append("<h2>"+nome+ "- 2010</h2><hr>");
          top10.forEach(function (d) {
            dummy.append('<p><span style="float:left">'+d['nome'] + '</span><span style="float:right">' + d['valor'] + '</span></p>');
          });
          dummy.append('<p><b><span style="float:left">Total</span><span style="float:right">' + data['total'] + '</span></b><p>')
          origin.tooltipster('content', dummy);
        });
      }
    });
  });
}

jQuery(document).ready(function($) {
  var texto = $("p").text().toUpperCase();
  console.log('Heyho, heyho!')
  var worker = new Worker(chrome.runtime.getURL('worker.js')); //Construct worker
  worker.onmessage = function (event) { //Listen for thread messages
    highlight(event.data);           //Log to the Chrome console
    console.log('Pra casa agora eu vou!');
  };
  worker.postMessage({'texto' : texto, 'nomes' : nick}); //Start the worker with args
});
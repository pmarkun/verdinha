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

function dummyRender(data) {
  var top10 = rank(data, 5);
  var dummy = $('<table>')
  dummy.append('<tr><th colspan="2">' + data.nome + ' - 2010</th></tr>');
  top10.forEach(function (d) {
    dummy.append('<tr><td>'+d['nome'] + '</td><td>' + d['valor'] + '</td></tr>');
  });
  dummy.append('<tr><td>Total: </td><td>' + data['total'] + '</td></tr>')
  dummy.append('</table>');
  return dummy
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
      theme: 'tooltipster-verdinha',
      
      functionBefore: function(origin, continueTooltip) {
        continueTooltip();

        $.getJSON("http://127.0.0.1:5000/busca/"+nome, function (data) {
          var dummy = dummyRender(data);
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
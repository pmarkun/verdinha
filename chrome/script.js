// JavaScript Document

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

jQuery(document).ready(function($) {
    console.log("Loaded!");
    console.log(nick);
    
    var texto = document.body.innerHTML;
    texto = texto.toUpperCase();
    matches = checaNomes(texto, nick);
    $.each(matches, function(key, value) {
      var nome_completo = key;
      if (value != 0) {
        nome_completo = value;
      }
      $("p").highlight(key, {caseSensitive: false, className: 'highlight-1337', wordsOnly:true, dataAttr: nome_completo});
    });
    $('.highlight-1337').each(function() {
        $(this).click(function () {
           var nome = $(this).attr("data-highlight");
           $.getJSON("http://127.0.0.1:5000/busca/"+nome, function (data) {
              console.log(data);
              
              // First create the array of keys/net_total so that we can sort it:
              var sort_array = [];
              for (var key in data.doacoes) {
                  sort_array.push({nome:data.doacoes[key].nome, valor:data.doacoes[key].valor});
              }

              // Now sort it:
              sort_array.sort(function(x,y){return x.valor - y.valor});
              
              var top10 = sort_array.reverse().slice(0,10);
              var dummy = nome+' 2010\n--------------------\n';
              top10.forEach(function (d) {
                dummy += d['nome'] + ' - ' + d['valor'] + '\n'
              });
              alert(dummy);
           })
        })
      var currentKey = $(this).text();
      });
});
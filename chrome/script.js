var BASE_URL = "http://verdinhas.org.br";
//var BASE_URL = "http://127.0.0.1:5000";

function refreshTooltip(origin) {
  $(".verdinha-click").click(function (e) {
            e.preventDefault();
            var _id = $(e.currentTarget).data('id');
            if (isNaN(_id)) {
              $.get(BASE_URL+"/busca/"+_id, function (data) {
                origin.tooltipster('content', $(data));
                refreshTooltip(origin);
              });
            }
            else {
              $.get(BASE_URL+"/cnpj/"+_id, function (data) {
                origin.tooltipster('content', $(data));
                refreshTooltip(origin);
              });
            }

          });
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
      content : $('<table><tr><th>Carregando...</th><th> </th></tr></table>'),
      interactive : true,
      arrow: false,
      theme: 'tooltipster-verdinha',

      functionBefore: function(origin, continueTooltip) {
        continueTooltip();
       $.get(BASE_URL+"/busca/"+nome, function (data) {
          origin.tooltipster('content', $(data));
          refreshTooltip(origin);
        });
      },


    });
  });
}

jQuery(document).ready(function($) {
  chrome.runtime.sendMessage({type: "disabled"}, function(response) {
    if(!response.disabled) {
      var texto = $("p").text().toUpperCase();
      var worker = new Worker(chrome.runtime.getURL('worker.js')); //Construct worker
      worker.onmessage = function (event) { //Listen for thread messages
        highlight(event.data);           //Log to the Chrome console
        console.log('Pra casa agora eu vou!');
      };
      worker.postMessage({'texto' : texto, 'nomes' : nick}); //Start the worker with args
    }
  });
});

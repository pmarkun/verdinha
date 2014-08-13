// JavaScript Document
jQuery(document).ready(function($) {
    console.log("Loaded!");
    console.log(nick);
    $.each(nick, function(key, value) {
      $("p").highlight(key, {caseSensitive: false, className: 'highlight-1337', wordsOnly:true });
    });
    $('.highlight-1337').each(function() {    
      var currentKey = $(this).text();
      });
});



function loadImmagini() 
{ 
   //Selezioniamo l'elemento canvas 
var canvas = document.getElementId("demo_canvas")
   //Verifichiamo che il browser supporti l'elemento 
   if (canvas.getContext) 
   { 
     //Creo un oggetto Canvas 
     var canv_ex = canvas.getContext("2d"); 
     //Disegno l'immagine da file esterno alla pagina
     var ps = new Image();
     ps.src = "upload/public/posa.jpg";
     canv_ex.drawImage(ps,0,0,ps.width/2,ps.height/2);

    //Disegno l'immagine da tag <img> con id = happy
    var hap = document.getElementById("happy");
    canv_ex.drawImage(hap,150,0,130,130,250,190,150,150);
   }
}

lanciaEvento = function(nome_evento){ 
  var evento = document.createEvent("CustomEvent"); 
  evento.initCustomEvent(nome_evento, true, true, titolo_fiveboard); 
  document.dispatchEvent(evento);
}

salvaAppunti = function(evento){ 
  localStorage.setItem("fb_" + evento.detail,
    document.forms['form_da_ricordare'].elements['testo_da_ricordare'].value 
  );
  alert("Appunti salvati");
}
 
recuperaAppunti = function(evento){ 
  document.forms['form_da_ricordare'].elements['testo_da_ricordare'].value =
localStorage.getItem("fb_" + evento.detail); 
  alert("Appunti recuperati");
}
 
document.addEventListener('salvadato', salvaAppunti); 
document.addEventListener('recuperadato', recuperaAppunti);
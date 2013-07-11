var ctx = null; 
var started = false;
 
iniziaDisegno = function(evento){ 
  ctx.beginPath(); 
  ctx.moveTo(evento.offsetX,evento.offsetY); 
  started = true;
}
 
disegna = function(evento){ 
  if(started){
    ctx.lineTo(evento.offsetX,evento.offsetY); 
    ctx.stroke();
  }
}
 
fermaDisegno = function(evento){ 
  ctx.closePath(); 
  started = false;
}
 
salvaCanvas = function(evento){ 
  localStorage.setItem("canvas_fb_" + evento.detail, ctx.canvas.toDataURL('image/png')); 
  alert("Canvas salvato");
}
 
recuperaCanvas = function(evento){ 
  var immagine_salvata = localStorage.getItem("canvas_fb_" + evento.detail); 
  if(immagine_salvata == null) return;
  var img = new Image(); 
  img.src = immagine_salvata; 
  ctx.canvas.width = ctx.canvas.width; 
  ctx.drawImage(img, 0, 0); 
  alert("Canvas recuperato");
}
 
attivaIlCanvas = function(evento){ 
  ctx = document.querySelector('canvas').getContext('2d');
  ctx.canvas.addEventListener('mousedown' , iniziaDisegno,false );
  ctx.canvas.addEventListener('mousemove' , disegna ,false );
  ctx.canvas.addEventListener('mouseup' ,   fermaDisegno ,false );
  ctx.canvas.addEventListener('mouseleave', fermaDisegno ,false );
  document.addEventListener('salvadato', salvaCanvas    ); 
  document.addEventListener('recuperadato', recuperaCanvas  );
} 
 
window.addEventListener('load' ,attivaIlCanvas,false);
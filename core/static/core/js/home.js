var urlSocket = 'ws://' + window.location.host + '/ws/camara/';
var camSocket = null;
var conectado = false;

$(function () {
	conectar();
});

function conectar() {
	if(!conectado){
		camSocket = new WebSocket(urlSocket);
		conectado = true;
		camSocket.onmessage = function(e) {
			var data = JSON.parse(e.data);
			recibir(data);
		};

		camSocket.onclose = function(e) {
			conectado = false;
			alert('Socket cerrado!');
		};
	}
}

function enviar(data) {
	camSocket.send(JSON.stringify({
		"data": data
	}));
}

function recibir(data) {
	var tipo = data['tipo'];
	if(tipo=="frame"){
		var img_src = data['img_src']
		$("#img-live").attr('src', img_src);
	}

	// console.log("Socket:" + message);
}

function on_off_streaming(btn){
	var btnOnOff = $(btn);
	
	if (btnOnOff.attr('estado') == 'off'){
		btnOnOff.attr('estado', 'on');
		btnOnOff.text('Detener');
		btnOnOff.removeClass('btn-success');
		btnOnOff.addClass('btn-danger');

		enviar("on");
	}else{
		btnOnOff.attr('estado', 'off');
		btnOnOff.text('Iniciar');
		btnOnOff.removeClass('btn-danger');
		btnOnOff.addClass('btn-success');

		enviar("off");
	}
}

function sleep(ms) {
	var now = new Date().getTime();
	while(new Date().getTime() < now + ms){} 
}
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
	switch(data['tipo']){
		case 'frame':
			$("#img-live").attr('src', data['img_src']);
			break;

		case 'tupla':
			agregarPlaca(data);
			break;
	}
}

function on_off_streaming(btn){
	if (configurado=='False') {
		alert("El sistema no está configurado, vaya a Configuración.");
		return;
	}

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

function agregarPlaca(data) {
	var fecha = '<td class="align-middle"><a href="#">'+data['fecha']+'</a></td>';
	var placa = '<td class="align-middle"><a href="#">'+data['placa']+'</a></td>';
	var img   = '<a href="#" title="Click para ver"><img class="img-mini" src="'+data['img_src']+'" alt="Placa"></a>';
	var imgTd = $('<td class="align-middle text-center img-td"></td>');
	var avisos= '<td class="align-middle text-center"><button class="btn btn-info">'+data['avisos']+'</button></td>'
	var row   = $("<tr></tr>");
	
	imgTd.prepend(img);  
	row.append(fecha, placa, imgTd, avisos);

	$('#tbl-placas tbody').prepend(row);  
	$('#tbl-placas tr:last').remove();
}

function sleep(ms) {
	var now = new Date().getTime();
	while(new Date().getTime() < now + ms){} 
}
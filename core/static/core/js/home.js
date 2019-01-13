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
	var clase = data['alerta_id'] ? 'btn-warning' : 'btn-default';
	var notificaciones = '<td class="align-middle text-center"><button class="btn '+clase+'" onclick="abrirModal('+data['alerta_id']+')">'+data['avisos']+'</button></td>'
	var row   = $("<tr></tr>");
	
	imgTd.prepend(img);  
	row.append(fecha, placa, imgTd, notificaciones);

	$('#tbl-placas tbody').prepend(row);  
	$('#tbl-placas tr:last').remove();
}

function sleep(ms) {
	var now = new Date().getTime();
	while(new Date().getTime() < now + ms){} 
}

function abrirModal(idAlerta) {
	if(!idAlerta){return;}
	getAlertaDetalle(idAlerta);
	$('#modalAlerta').modal('toggle');
}

function actualizarModal(){
	var idAlerta = $("#idAD").text();
	getAlertaDetalle(idAlerta);
}

function getAlertaDetalle(idAlerta){
	$.ajax({
		method: "POST",
		url: '/get_alerta_detalle',
		data: {
			'id': idAlerta,
			'csrfmiddlewaretoken': csrfToken
		}
	})
	.done(function(response) {
		console.log(response);
		$("#idAD").text(response.id_alerta);
		$("#fechaEmisionAD").text(response.fecha_emision);
		$("#matriculaAD").text(response.matricula);
		$("#direccionAD").text(response.direccion);
		$("#imagenAD").attr('src', response.imagen);

		$("#tblNotificacionesAD tbody").remove();

		var notificaciones = response.notificaciones;

		if (notificaciones){
			var tbody = $("<tbody></tbody>");

			for (var i = 0; i < notificaciones.length; i++) {
				var tr = $("<tr></tr>");

				var id = '<td class="align-middle">'+notificaciones[i].id+'</td>';
				var patrullero = '<td class="align-middle">'+notificaciones[i].patrullero+'</td>';
				var is_entregada = notificaciones[i].entregada?'Sí':'No';
				var entregada = '<td class="align-middle">'+ is_entregada +'</td>';
				var is_alcanzado = notificaciones[i].alcanzado?'Sí':'No';
				var alcanzado = '<td class="align-middle">'+ is_alcanzado +'</td>';
				var is_atendida = notificaciones[i].atendida?"Sí":"No";
				var atendida = '<td class="align-middle">'+ is_atendida +'</td>';
				var fecha_entregada = '<td class="align-middle">'+notificaciones[i].fecha_entregada+'</td>';
				var fecha_atendida = '<td class="align-middle">'+notificaciones[i].fecha_atendida+'</td>';

				tr.append(id, patrullero, entregada, alcanzado, atendida, fecha_entregada, fecha_atendida);

				tbody.append(tr);
			}

			$("#tblNotificacionesAD").append(tbody);
		}
	})
	.fail(function(xhr, status, error){
		console.log("Error");
	});
}
var urlSocket = 'ws://' + window.location.host + '/ws/config/';
var camSocket = null;
var conectado = false;

$(function () {
	conectar();
	getPeaje();
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

function recibir(data) {
	$("#img-live").attr('src', data['img_src']);
}

function limpiarPeaje(){
	peajeValido = false;
	$("#nombrePeaje").text('');
	$("#longitudPeaje").text('');
	$("#latitudPeaje").text('');
	$("#radioPeaje").text('');
}

function getPeaje() {
	limpiarPeaje();
	id = $("#txtIdPeaje").val();

	if (isNaN(id)){return;}

	$.ajax({
		url: '/api/peajes/'+id,
	})
	.done(function(peaje, status, code) {
		$("#nombrePeaje").text(peaje.nombre);
		$("#longitudPeaje").text(peaje.longitud);
		$("#latitudPeaje").text(peaje.latitud);
		$("#radioPeaje").text(peaje.radio);
		peajeValido = true;
	})
	.fail(function(xhr, status, error){
		peajeValido = false;
	});
}

function setPeaje() {
	id = $("#txtIdPeaje").val();

	if (peajeValido && id){
		$.ajax({
			method: "POST",
			url: '/configurar_peaje',
			data: {
				'id': id.trim(),
				'csrfmiddlewaretoken': csrfToken
			}
		})
		.done(function(peaje, status, code) {
			$("#estadoPeaje").text('Configurado');
			$("#estadoPeaje").removeClass('text-danger');
			$("#estadoPeaje").addClass('text-success');
		})
		.fail(function(xhr, status, error){
			alert("Error al configurar peaje")
		});
	} else {
		alert("Id de peaje inválido");
	}
}

function setCamara() {
	direccion = $("#txtDireccionCamara").val();
	
	if (direccion){
		$.ajax({
			method: "POST",
			url: '/configurar_camara',
			data: {
				'direccion': direccion.trim(),
				'csrfmiddlewaretoken': csrfToken
			}
		})
		.done(function(peaje, status, code) {
			$("#estadoCamara").text('Configurado');
			$("#estadoCamara").removeClass('text-danger');
			$("#estadoCamara").addClass('text-success');
		})
		.fail(function(xhr, status, error){
			alert("Error al configurar camara")
		});
	} else {
		alert("Debe ingresar una dirección para la cámara");
	}
}
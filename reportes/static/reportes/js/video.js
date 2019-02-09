function mostrarVideo(video_url, placa, direccion, fecha) {
	try {
		ruta = media_url+"/"+video_url
		$("video").attr("src", ruta).load().play();
	}catch(e){}
	
	$("#modal-titulo").text(placa + " | " + direccion + " | " + fecha);
	$("#modal-video").modal().toggle();
}


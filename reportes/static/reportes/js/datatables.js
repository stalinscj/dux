$(function () {
	$('#tbl-reporte').DataTable({
		"language": {
			"emptyTable"   : "No hay registros disponibles en esta tabla",
			"info"         : "Mostrando del _START_ al _END_ de _TOTAL_ registros",
			"infoEmpty"    : "Mostrando del 0 al 0 de 0 registros",
			"infoFiltered" : "(filtrado de _MAX_ registros en total)",
			"lengthMenu"   : "Mostrar _MENU_ registros por página",
			"zeroRecords"  : "No se encontraron coincidencias",
			"search"       : "Buscar:",
			"paginate"     : {
				"first"    : "Primero",
				"last"     : "Último",
				"next"     : "Siguiente",
				"previous" : "Anterior"
			},
		},
		"dom": 'Bfrtip',
		"buttons": [
		    'pdf', 'excel', 'csv'
		]
	});
});
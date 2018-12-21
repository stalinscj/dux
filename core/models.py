from django.utils.timezone import now
from django.db import models
from pyfcm import FCMNotification

class Peaje(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre')
	latitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitud', help_text="Puede conocer la latitud en Google Maps; Click Derecho -> ¿Qué hay aquí?")
	longitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitud', help_text="Puede conocer la latitud en Google Maps; Click Derecho -> ¿Qué hay aquí?")
	radio = models.DecimalField(max_digits=10, decimal_places=3, help_text="Indique el radio (en metros) de acción para el envío de notificaciones")

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Lectura(models.Model):
	peaje       = models.ForeignKey(Peaje, on_delete=models.PROTECT, verbose_name='Peaje')
	fecha       = models.DateTimeField(default=now, verbose_name='Fecha')
	matricula   = models.CharField(max_length=7, verbose_name='Matrícula')
	direccion   = models.CharField(max_length=50, verbose_name='Dirección')
	imagen      = models.TextField(verbose_name='Img')
	imagen_mini = models.TextField(verbose_name='Img (min)')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return self.matricula

	def save(self, *args, **kwargs):
		self.matricula = self.matricula.upper()
		return super(Lectura, self).save(*args, **kwargs)

class Patrullero(models.Model):
	cedula = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
	nombre = models.CharField(max_length=100, verbose_name='Nombre')
	activo = models.BooleanField(default=False, verbose_name="Activo")
	token  = models.CharField(max_length=250, verbose_name='Token')

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Alerta(models.Model):
	lectura     = models.ForeignKey(Lectura, on_delete=models.PROTECT, verbose_name='Lectura')
	fecha       = models.DateTimeField(default=now, verbose_name='Fecha')
	notificados = models.ManyToManyField(Patrullero, through='Notificado')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return self.lectura.matricula

	def nueva(solicitud, lectura):
		peaje = lectura.peaje
		alerta = Alerta.objects.create(lectura = lectura)

		mensaje = {
			'alerta_id': alerta.pk,
			'latitud': str(peaje.latitud),
			'longitud': str(peaje.longitud),
			'radio': str(peaje.radio)
		}

		registration_ids = []

		patrulleros = Patrullero.objects.filter(activo=True)
		print(patrulleros)
		for patrullero in patrulleros:
			registration_ids.append(patrullero.token)
			
		push_service = FCMNotification(api_key="AIzaSyBCr-rmINKdZQUKT3rQmLolkeFX4iNaB7c")
		
		result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=mensaje)

		if result['success']==1:
			for patrullero in patrulleros:
			 	Notificado.objects.create(alerta=alerta, patrullero=patrullero) 
		else:
			Alerta.objects.filter(pk=alerta.pk).delete()
			print("\nError al enviar las notificaciones\n")
			print(result)


class Notificado(models.Model):
	alerta          = models.ForeignKey(Alerta, on_delete=models.PROTECT, verbose_name='Alerta')
	patrullero      = models.ForeignKey(Patrullero, on_delete=models.PROTECT, verbose_name='Patrullero')
	entregada       = models.BooleanField(default=False, verbose_name="Entregada")
	alcanzado       = models.BooleanField(default=False, verbose_name="Alcanzado")
	atendida        = models.BooleanField(default=False, verbose_name="Atendida")
	fecha_entregada = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Entregada')
	fecha_atendida  = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Atendida')

	class Meta:
		ordering = ['-alerta']

	def __str__(self):
		return "{} - {}".format(self.alerta, self.patrullero)


class MatriculaSolicitada(models.Model):
	matricula        = models.CharField(max_length=7, verbose_name='Matrícula')
	fecha_solicitada = models.DateTimeField(verbose_name='Fecha Solicitud')
	motivo           = models.CharField(max_length=50, verbose_name='Motivo')
	activo           = models.BooleanField(verbose_name="Activo")

	class Meta:
		verbose_name_plural='Matrículas Solicitadas'
		ordering = ['-fecha_solicitada']

	def __str__(self):
		return "{} - {}".format(self.matricula, self.fecha_solicitada)

	def save(self, *args, **kwargs):
		self.matricula = self.matricula.upper()
		return super(MatriculaSolicitada, self).save(*args, **kwargs)


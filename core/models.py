from django.utils.timezone import now
from django.db import models
from pyfcm import FCMNotification

class Peaje(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre')
	# ciudad = models.CharField(max_length=100, verbose_name='Ciudad')

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
		push_service = FCMNotification(api_key="AIzaSyBCr-rmINKdZQUKT3rQmLolkeFX4iNaB7c")
		registration_id = "dFxnUETLIlI:APA91bEBsD8x_1CcJOHY6lYOwcOM-oAbBddDPspzBClPV3AlVrgdFPUllQV_18cOEw_iaYvEJAhGXAfp_kZ2v5bCeNSU3DYvpsucLnGfW_HJPAbNwqvYb5ul7HTtyfri3aNnde7w9lSb"
		# message_title = "Matrícula {} Solicitada".format(lectura.matricula)
		# message_body = "Esta matrícula pasó por el peaje {} con dirección {}".format(lectura.peaje, lectura.direccion)
		# result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		mensaje = {
			'alerta_id': 1,
			'lectura_id': 305,
			'fecha' : '2018-12-31 11:59:00'
		}
		
		result = push_service.single_device_data_message(registration_id=registration_id, data_message=mensaje)
		
		print("\n\n")
		print(result)
		print("\n\n")

		if result['success']==1:
			alerta = Alerta.objects.create(lectura = lectura)
			patrulleros = Patrullero.objects.filter(activo=True)
			for patrullero in patrulleros:
			 	Notificado.objects.create(alerta=alerta, patrullero=patrullero) 
		else:
			print("\n\nError\n\n")


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


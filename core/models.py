from django.utils.timezone import now
from django.db import models

class Peaje(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre')
	ciudad = models.CharField(max_length=100, verbose_name='Ciudad')

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return "{} - {}".format(self.nombre, self.ciudad)


class Lectura(models.Model):
	peaje       = models.ForeignKey(Peaje, on_delete=models.PROTECT, verbose_name='Peaje')
	fecha       = models.DateTimeField(default=now, verbose_name='Fecha')
	matricula   = models.CharField(max_length=7, verbose_name='Matrícula')
	imagen      = models.TextField(verbose_name='Img')
	imagen_mini = models.TextField(verbose_name='Img (min)')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return self.matricula


class Patrullero(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre')
	activo = models.BooleanField(verbose_name="Activo")

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Alerta(models.Model):
	peaje       = models.ForeignKey(Peaje, on_delete=models.PROTECT, verbose_name='Peaje')
	fecha       = models.DateTimeField(default=now, verbose_name='Fecha')
	notificados = models.ManyToManyField(Patrullero, through='Notificado')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return "{} - {}".format(self.peaje, self.fecha)


class Notificado(models.Model):
	alerta          = models.ForeignKey(Alerta, on_delete=models.PROTECT, verbose_name='Alerta')
	patrullero      = models.ForeignKey(Patrullero, on_delete=models.PROTECT, verbose_name='Patrullero')
	entregada       = models.BooleanField(verbose_name="Entregada")
	alcanzado       = models.BooleanField(verbose_name="Alcanzado")
	atendida        = models.BooleanField(verbose_name="Atendida")
	fecha_entregada = models.DateTimeField(null=True, verbose_name='Fecha Entregada')
	fecha_atendida  = models.DateTimeField(null=True, verbose_name='Fecha Atendida')

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
			ordering = ['-fecha_solicitada']

	def __str__(self):
		return "{} - {}".format(self.matricula, self.fecha_solicitada)


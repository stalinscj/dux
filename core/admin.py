from .models import Alerta, Lectura, MatriculaSolicitada, Notificacion, Patrullero, Peaje
from django.conf.locale.es import formats as es_formats
from django.contrib import admin

es_formats.DATETIME_FORMAT = "d/m/Y H:i:s"

# Register your models here.
class PeajeAdmin(admin.ModelAdmin):
	search_fields = ('nombre', )
	list_display = ( 'id', 'nombre', 'longitud', 'latitud', 'radio' )
	ordering = ( 'nombre',)


class LecturaAdmin(admin.ModelAdmin):
	search_fields = ('matricula', 'fecha', 'direccion')
	list_display = ( 'fecha', 'matricula', 'peaje', )
	ordering = ( '-fecha',)
	list_filter = ('peaje', )


class PatrulleroAdmin(admin.ModelAdmin):
	search_fields = ('cedula', 'nombre')
	list_display = ( 'cedula', 'nombre', 'activo', )
	ordering = ( 'nombre',)
	list_filter = ('activo', )


class AlertaAdmin(admin.ModelAdmin):
	list_display = ( 'fecha', 'lectura', )
	ordering = ( '-fecha',)


class NotificacionAdmin(admin.ModelAdmin):
	search_fields = ('peaje', 'matricula', 'patrullero', 'fecha_emitida', 'fecha_entregada', 'fecha_atendida', )
	list_display = ( 'id', 'peaje', 'fecha_emitida', 'matricula', 'patrullero', 'entregada', 'alcanzado', 'atendida', 'fecha_entregada', 'fecha_atendida', )
	ordering = ( '-id', )
	list_filter = ('entregada', 'alcanzado', 'atendida', )

	def peaje(self, obj):
		return obj.alerta.lectura.peaje.nombre

	def fecha_emitida(self, obj):
		return obj.alerta.fecha

	def matricula(self, obj):
		return obj.alerta.lectura.matricula


class MatriculaSolicitadaAdmin(admin.ModelAdmin):
	search_fields = ('matricula', 'motivo', 'activo', )
	list_display = ('matricula', 'fecha_solicitada', 'motivo', 'activo', )
	ordering = ('matricula', )
	list_filter = ('activo', )


admin.site.register(Peaje, PeajeAdmin)
admin.site.register(Alerta, AlertaAdmin)
admin.site.register(Lectura, LecturaAdmin)
admin.site.register(MatriculaSolicitada, MatriculaSolicitadaAdmin)
admin.site.register(Notificacion, NotificacionAdmin)
admin.site.register(Patrullero, PatrulleroAdmin)

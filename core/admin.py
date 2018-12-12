from .models import Alerta, Lectura, MatriculaSolicitada, Notificado, Patrullero, Peaje
from django.contrib import admin

# Register your models here.
class PeajeAdmin(admin.ModelAdmin):
	pass


class LecturaAdmin(admin.ModelAdmin):
	pass


class PatrulleroAdmin(admin.ModelAdmin):
	pass


class AlertaAdmin(admin.ModelAdmin):
	pass


class NotificadoAdmin(admin.ModelAdmin):
	pass


class MatriculaSolicitadaAdmin(admin.ModelAdmin):
	pass


admin.site.register(Peaje, PeajeAdmin)
admin.site.register(Alerta, AlertaAdmin)


admin.site.register(Lectura, LecturaAdmin)
admin.site.register(MatriculaSolicitada, MatriculaSolicitadaAdmin)
admin.site.register(Notificado, NotificadoAdmin)
admin.site.register(Patrullero, PatrulleroAdmin)

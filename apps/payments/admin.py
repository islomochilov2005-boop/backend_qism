from django.contrib import admin
from .models import Paket, Tolov

@admin.register(Paket)
class PaketAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'narx', 'faol', 'yaratilgan']
    list_filter = ['faol']

@admin.register(Tolov)
class TolovAdmin(admin.ModelAdmin):
    list_display = ['id', 'foydalanuvchi', 'mashina', 'summa', 'holat', 'yaratilgan']
    list_filter = ['holat', 'yaratilgan']
    search_fields = ['foydalanuvchi__username']
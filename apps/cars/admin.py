from django.contrib import admin
from .models import Mashina, MashinaRasm, Sevimli

class MashinaRasmInline(admin.TabularInline):
    model = MashinaRasm
    extra = 1

@admin.register(Mashina)
class MashinaAdmin(admin.ModelAdmin):
    list_display = ['marka', 'model', 'yil', 'narx', 'holat', 'yaratilgan']
    list_filter = ['holat', 'ahvol', 'marka']
    search_fields = ['marka', 'model']
    inlines = [MashinaRasmInline]

admin.site.register(MashinaRasm)
admin.site.register(Sevimli)
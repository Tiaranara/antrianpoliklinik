from django.contrib import admin
from .models import Poli, Dokter, Pasien, Antrian

@admin.register(Poli)
class PoliAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)

@admin.register(Dokter)
class DokterAdmin(admin.ModelAdmin):
    list_display = ('nama', 'poli', 'jadwal')
    list_filter = ('poli',)
    search_fields = ('nama',)

@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_rekam_medis', 'nik', 'no_telepon')
    search_fields = ('nama', 'nik', 'no_rekam_medis')

@admin.register(Antrian)
class AntrianAdmin(admin.ModelAdmin):
    list_display = ('nomor_antrian', 'pasien', 'poli', 'dokter', 'tanggal', 'waktu_kunjungan', 'status')
    list_filter = ('tanggal', 'poli', 'status')
    search_fields = ('pasien__nama', 'pasien__nik')

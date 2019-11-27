from django.contrib import admin
from customadmin.models import *
from customadmin.form import *
from django import forms
from django.contrib.auth.models import Group

class pelajaran(admin.ModelAdmin):
    list_display = ['nama_pelajaran']
    search_fields = ['nama_pelajaran']
    list_per_page = 5

class materi(admin.ModelAdmin):
    list_display = ['nama_materi','pelajaran','File_Pdf','status']
    list_filter = ['pelajaran']
    search_fields = ['nama_materi']
    list_per_page = 5

class profil(admin.ModelAdmin):
    list_display = ['akun','nama','alamat','sekolah','kelas','angkatan']
    search_fields = ['nama']
    list_filter = ['kelas__nama_kelas','angkatan__nama_angkatan']
    list_per_page = 5
    form = Profil_form_admin

class HiddenModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms

class kuis(admin.ModelAdmin):
    list_display = ['nama_kuis','pelajaran']
    filter_horizontal = ('soal',)
    list_per_page = 5

class soal(admin.ModelAdmin):
    list_display = ['soal','pelajaran']
    list_filter = ['pelajaran']
    search_fields = ['soal']
    list_per_page = 5

class nilai(admin.ModelAdmin):
    list_display = ['nama','kelas','kuis','nilai','created_at']
    list_filter = ('kuis__nama_kuis','nama__nama','nama__kelas')
    def kelas(self, obj):
            return obj.nama.kelas
class angkatan(admin.ModelAdmin):
    list_display = ['nama_angkatan','tahun']
    list_per_page = 5
    form = Angkatan_form_admin

admin.site.register(Materi,materi)
admin.site.register(Soal,soal)
admin.site.register(Kuis,kuis)
admin.site.register(Nilai,nilai)
admin.site.register(Pelajaran,pelajaran)
admin.site.register(Siswa,profil)
admin.site.register(Angkatan,angkatan)
admin.site.register(Kelas)

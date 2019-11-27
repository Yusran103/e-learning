from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import truncatechars

# Create your models here.

class Pelajaran(models.Model):
    id_pelajaran = models.AutoField(primary_key=True)
    nama_pelajaran = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_pelajaran"
        verbose_name_plural = "Pelajaran"
    
    def __str__(self):
        return self.nama_pelajaran

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_kelas"
        verbose_name_plural = "Kelas"
    
    def __str__(self):
        return self.nama_kelas

def current_year():
    return datetime.date.today().year

def yearchoice(value):
    return MaxValueValidator(current_year())(value)

class Angkatan(models.Model):
    nama_angkatan = models.CharField(max_length=50)
    tahun = models.IntegerField(validators=[MinValueValidator(2000),yearchoice])
    
    class Meta:
        db_table = "tb_angkatan"
        verbose_name_plural = "Angkatan"
    
    def __str__(self):
        return self.nama_angkatan

class Materi(models.Model):
    id_materi = models.AutoField(primary_key=True)
    nama_materi = models.CharField(max_length=50)
    pelajaran = models.ForeignKey(Pelajaran, db_column='id_pelajaran', on_delete=models.CASCADE)
    File_Pdf = models.FileField(upload_to='materi',null=True,blank=True, max_length=100)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "tb_materi"
        verbose_name_plural = "Materi"
    
    def __str__(self):
        return self.nama_materi
    
    def delete(self, *args, **kwargs):
        os.remove("materi/%s"%os.path.join(setings.MEDIA_ROOT, self.File_Pdf.name))
        super(Materi,self).delete(*args, **kwargs)

class Soal(models.Model):
    PILIHAN_CHOICES = [
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
    ]
    
    id_soal = models.AutoField(primary_key=True)
    pelajaran = models.ForeignKey(Pelajaran, db_column='id_pelajaran', on_delete=models.CASCADE)
    soal = models.TextField()
    a = models.TextField()
    b = models.TextField()
    c= models.TextField()
    d= models.TextField()
    benar= models.CharField(max_length=1, choices=PILIHAN_CHOICES, default='a')

    class Meta:
        db_table = "tb_soal"
        verbose_name_plural = "Soal"

    @property
    def short_description(self):
        return truncatechars(self.soal, 30)
    
    def __str__(self):
        return "%s | %s"%(self.short_description,self.pelajaran)

class Kuis(models.Model):
    id_kuis = models.AutoField(primary_key=True)
    nama_kuis = models.CharField(max_length=50)
    pelajaran = models.ForeignKey(Pelajaran, db_column='id_pelajaran', on_delete=models.CASCADE)
    soal = models.ManyToManyField(Soal, db_column='id_soal', verbose_name="Soal")
    class Meta:
        db_table = "tb_kuis"
        verbose_name_plural = "Kuis"

    def __str__(self):
        return str(self.nama_kuis)

class Siswa(models.Model):
    """docstring for user"""
    USER_CHOICES = [
        ('Siswa', 'Siswa'),
    ]
    akun = models.OneToOneField(
        User,
        on_delete=models.CASCADE,primary_key=True,
    )
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    nama_bapak = models.CharField(max_length=100)
    nama_ibu = models.CharField(max_length=100)
    sekolah = models.CharField(max_length=100)
    alamat_sekolah = models.TextField()
    level = models.CharField(max_length=20, choices=USER_CHOICES, default='Siswa')
    kelas = models.ForeignKey(Kelas,db_column='kelas', on_delete=models.CASCADE)
    angkatan = models.ForeignKey(Angkatan,db_column='angkatan', on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

    class Meta:
        db_table = "tb_siswa"
        verbose_name_plural = "Siswa"

class Nilai(models.Model):
    id_nilai = models.AutoField(primary_key=True)
    kuis = models.ForeignKey(Kuis, db_column='id_kuis', on_delete=models.CASCADE)
    nama = models.ForeignKey(Siswa,db_column='id_profil',on_delete=models.CASCADE)
    nilai = models.IntegerField(validators=[MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_nilai"
        verbose_name_plural = "Nilai"

    def __str__(self):
        return "%s | %s"%(self.nama,self.kuis)
    
    def date(self):
        return self.created_at.strftime('%d %b %Y')


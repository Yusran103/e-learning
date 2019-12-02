from django.shortcuts import render, get_object_or_404 ,redirect
from customadmin.models import *
from django.http import HttpResponse,FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages, auth
from customadmin.form import Profile_form, User_form
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Avg
from rest_framework import generics
from .models import Nilai
from .serializers import *
from django.core import serializers
from django.core.serializers import serialize 
from datetime import datetime

# Create your views here.
@login_required(login_url='/login')
def index(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render(request, 'index.html')
# Login
def Login(request):
    if request.POST:
        users = authenticate(username=request.POST['login_username'], password=request.POST['login_password'])
        if users is not None:
            if not users.is_staff:
                try:
                    profil = Siswa.objects.get(akun_id=users.id)
                    login(request, users)
                    request.session['nama'] = profil.nama
                    request.session['level'] = profil.level
                    request.session['id'] = users.id
                    return redirect('/')
                except Siswa.DoesNotExist:
                    messages.add_message(request, messages.INFO, 'Akun Tersebut Belum Memiliki Profil, Silahkan Hubungi Admin')  
            else:
               messages.add_message(request, messages.INFO, 'Akun Tersebut Bukan Termasuk Akun Siswa') 
        else:
            messages.add_message(request, messages.INFO, 'Username atau password Anda salah')
    return render(request, 'login.html')

# LOGOUT
def Logout(request):
    logout(request)
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

# CHANGEPASSWORD 
@login_required(login_url='/')
def changepassword(request,pk):
    user = User.objects.filter(id = request.session['id']).first()
    if request.method == "POST":
        form = User_form(request.POST, instance=user)
        if form.is_valid():
            url = '/'
            resp_body = '<script>alert("Password user %s Berhasil di rubah, Silahkan Login Kembali");\
            window.location="%s"</script>' % (user.username , url)
            cursor = connection.cursor()
            cursor.execute("update auth_user set password='%s' where id='%s'"%(make_password(request.POST['password']),user.id))
            return HttpResponse(resp_body)
    else:
        form = User_form(instance=user)
    return render(request, 'changepassword.html', {'form': form, 'user' : user,'messages':messages})

@login_required(login_url='/')
def changeprofile(request,pk):
    user = Siswa.objects.filter(akun_id = request.session['id']).first()
    if request.method == "POST":
        form = Profile_form(request.POST, instance=user)
        if form.is_valid():
            url = '/'
            resp_body = '<script>alert("Profil user %s Berhasil di rubah");\
            window.location="%s"</script>' % (user.nama , url)
            cursor = connection.cursor()
            cursor.execute(
                """update tb_siswa set 
                    nama='%s',
                    alamat='%s',
                    nama_bapak='%s',
                    nama_ibu='%s',
                    sekolah='%s',
                    alamat_sekolah='%s' where akun_id ='%s' """
                    %(
                        request.POST['nama'],
                        request.POST['alamat'],
                        request.POST['nama_bapak'],
                        request.POST['nama_ibu'],
                        request.POST['sekolah'],
                        request.POST['alamat_sekolah'],
                        user.akun_id
                    )
                )
            request.session['nama'] = user.nama
            return HttpResponse(resp_body)
    else:
        form = Profile_form(instance=user)
    return render(request, 'changeprofile.html', {'form': form, 'user' : user,'messages':messages})

@login_required(login_url='/login')
def mainbi(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Bahasa Indonesia")
    ambil_materi = Materi.objects.filter(pelajaran=ambilpelajaran.id_pelajaran,status=True)
    request.session['BI'] = request.POST.get('materi')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render (request,'materi/BI/view_materi_bi.html',{'ambil_materi':ambil_materi})

@login_required(login_url='/login')
def pdfbi(request):
    ambil_pdf = "materi/%s"%request.session['BI']
    print(ambil_pdf)
    try:
        return FileResponse(open(ambil_pdf, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        return FileResponse(open('materi/materi/Document1.pdf', 'rb'), content_type='application/pdf')

@login_required(login_url='/login')
def mainipa(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Ilmu Pengetahuan Alam")
    ambil_materi = Materi.objects.filter(pelajaran=ambilpelajaran.id_pelajaran,status=True)
    request.session['IPA'] = request.POST.get('materi')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render (request,'materi/IPA/view_materi_ipa.html',{'ambil_materi':ambil_materi})

@login_required(login_url='/login')
def pdfipa(request):
    ambil_pdf = "materi/%s"%request.session['IPA']
    print(ambil_pdf)
    try:
        return FileResponse(open(ambil_pdf, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        return FileResponse(open('materi/materi/Document1.pdf', 'rb'), content_type='application/pdf')

@login_required(login_url='/login')
def mainmm(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Matematika")
    ambil_materi = Materi.objects.filter(pelajaran=ambilpelajaran.id_pelajaran,status=True)
    request.session['MM'] = request.POST.get('materi')
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    return render (request,'materi/MM/view_materi_mm.html',{'ambil_materi':ambil_materi})

@login_required(login_url='/login')
def pdfmm(request):
    ambil_pdf = "materi/%s"%request.session['MM']
    print(ambil_pdf)
    try:
        return FileResponse(open(ambil_pdf, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        return FileResponse(open('materi/materi/Document1.pdf', 'rb'), content_type='application/pdf')

@login_required(login_url='/login')
def kuisipa(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Ilmu Pengetahuan Alam")
    list_kuis_ipa = Kuis.objects.filter(pelajaran=ambilpelajaran.id_pelajaran)
    return render(request,'kuis/IPA/view_kuis_ipa.html',{'list_kuis_ipa':list_kuis_ipa})


@login_required(login_url='/login')
def kuisbi(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Bahasa Indonesia")
    list_kuis_bi = Kuis.objects.filter(pelajaran=ambilpelajaran.id_pelajaran)
    return render(request,'kuis/BI/view_kuis_bi.html',{'list_kuis_bi':list_kuis_bi})

@login_required(login_url='/login')
def kuismm(request):
    ambilpelajaran = Pelajaran.objects.get(nama_pelajaran = "Matematika")
    list_kuis_mm = Kuis.objects.filter(pelajaran=ambilpelajaran.id_pelajaran)
    return render(request,'kuis/MM/view_kuis_mm.html',{'list_kuis_mm':list_kuis_mm})

@login_required(login_url='/login')
def soal(request):
    ambil_kuis = request.POST.get('kuis')
    if ambil_kuis == None:
        resp_body = '<script>\
            alert("Silahkan Pilih Kuis");\
            window.history.back();</script>'
        return HttpResponse(resp_body)
    else:        
        cek_kuis = Kuis.objects.get(id_kuis=ambil_kuis)
        ambil_soal = cek_kuis.soal.order_by("?")
    return render(request,'kuis/list_soal.html',{'nama_pelajaran':cek_kuis,'list_soal':ambil_soal})

def nilai(request):
    ambilsesisiswa = request.session['id']
    ambilnilaisiswa = Nilai.objects.filter(nama_id = ambilsesisiswa)
    rataratanilai = ambilnilaisiswa.aggregate(Avg('nilai'))
    return render(request,'nilai/nilai.html',{'nilai':ambilnilaisiswa,'ratarata':rataratanilai})

def printnilai(request,pk):
    ambilidnilai = Nilai.objects.get(pk=pk)
    ambilkuis = Kuis.objects.get(nama_kuis = ambilidnilai.kuis)
    ambilprofil = Siswa.objects.get(akun_id=ambilidnilai.nama)
    asd = "%s , %s" % (ambilprofil,ambilkuis)
    
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y%m%d%H%M%S")
    # return HttpResponse(asd)
    return render(request,'nilai/print.html',{'nilai':ambilidnilai,'kuis':ambilkuis,'profil':ambilprofil,'date':formatedDate})

class NilaiList(generics.ListCreateAPIView):
    queryset = Nilai.objects.all()
    serializer_class = NilaiSerializer

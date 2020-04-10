"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from customadmin import views as customadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    # LOGIN
    path('', customadmin.index, name ='index'),
    path('login', customadmin.Login, name='Login'),
    path('logout',customadmin.Logout, name='Logout'),
    # CHANGE PASSWORD
    path('changepassword/<int:pk>', customadmin.changepassword, name='changepassword'),
    path('changeprofile/<int:pk>', customadmin.changeprofile, name='changeprofile'),
    # MATERI
    path('materi/BI', customadmin.mainbi, name='mainbi'),url('pdfbi', customadmin.pdfbi, name='pdfbi'),
    path('materi/IPA', customadmin.mainipa, name='mainipa'),url('pdfipa', customadmin.pdfipa, name='pdfipa'),
    path('materi/MM', customadmin.mainmm, name='mainmm'),url('pdfmm', customadmin.pdfmm, name='pdfmm'),
    # KUIS
    path('kuis/IPA',customadmin.kuisipa, name="kuisipa"),
    path('kuis/BI',customadmin.kuisbi, name="kuisbi"),
    path('kuis/MM',customadmin.kuismm, name="kuismm"),
    # SOAL
    path('kuis/IPA/soal',customadmin.soal, name="soalipa"),
    path('kuis/BI/soal',customadmin.soal, name="soalbi"),
    path('kuis/MM/soal',customadmin.soal, name="soalmm"),
    # CEK NILAI VIA rest_framework
    path('nilai', customadmin.NilaiList.as_view(), name="nilai"),
    path('nilaikuis', customadmin.nilai, name="nilaikuis"),
    path('print/<int:pk>',customadmin.printnilai, name="printnilai"),
]

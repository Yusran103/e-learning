from django.contrib.auth.models import User
from django.forms import Textarea, ModelForm, Select
from django import forms
from customadmin.models import *
# ----------+
# User FORM |
# ----------+
class Profile_form(ModelForm):
    nama = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan nama'
                }
            ),
            required=True
        )
    alamat = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Alamat',
                'rows':'2',
            }
        ),
        required=True
    )
    nama_bapak = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan nama bapak'
                }
            ),
            required=True
        )
    nama_ibu = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan username'
                }
            ),
            required=True
        )
    sekolah = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan nama sekolah'
                }
            ),
            required=True
        )
    kelas = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan nama kelas'
                }
            ),
            required=True
        )
    angkatan = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan nama angkatan'
                }
            ),
            required=True
        )
    alamat_sekolah = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Alamat Sekolah',
                'rows':'2',
            }
        ),
        required=True
    )
    class Meta:
        model = Siswa
        fields = [
            'nama',
            'alamat',
            'nama_bapak',
            'nama_ibu',
            'sekolah',
            'kelas',
            'angkatan',
            'alamat_sekolah',
        ]

class User_form(ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan username'
                }
            ),
            required=True
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Isikan password'
                }
            ),
            required=True
        )
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
class Profil_form_admin(ModelForm):
    akun = forms.ModelChoiceField(
        queryset = User.objects.filter(is_staff=False),
        widget = Select(
            attrs = {
                'class':'form-control',
            }
        )
    )
    class Meta:
        model = Siswa
        fields = "__all__"

def year_choices():
    return [(r,r) for r in range(2000,datetime.date.today().year+1)]

class Angkatan_form_admin(ModelForm):
    tahun = forms.TypedChoiceField(coerce=int,choices=year_choices,initial=current_year)

    class Meta:
        model = Angkatan
        fields = "__all__"
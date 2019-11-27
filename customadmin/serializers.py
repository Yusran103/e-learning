from rest_framework import serializers
from .models import *


class NilaiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nilai
        fields = ('id_nilai', 'kuis', 'nama', 'nilai','created_at')
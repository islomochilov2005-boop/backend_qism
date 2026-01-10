from rest_framework import serializers
from .models import Paket, Tolov

class PaketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paket
        fields = ['id', 'nomi', 'narx', 'tavsif']


class TolovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolov
        fields = ['id', 'mashina', 'paket', 'summa', 'holat', 'yaratilgan']


class TolovYaratishSerializer(serializers.Serializer):
    mashina_id = serializers.IntegerField()
    paket_id = serializers.IntegerField()
from rest_framework import serializers
from .models import Mashina, MashinaRasm, Sevimli


class MashinaRasmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MashinaRasm
        fields = ['id', 'rasm', 'asosiy']


class MashinaSerializer(serializers.ModelSerializer):
    rasmlar = MashinaRasmSerializer(many=True, read_only=True)
    asosiy_rasm = serializers.SerializerMethodField()
    sevimli = serializers.SerializerMethodField()

    class Meta:
        model = Mashina
        fields = ['id', 'marka', 'model', 'yil', 'narx', 'probeg', 'ahvol', 'rang',
                  'viloyat', 'tavsif', 'holat', 'korilganlar', 'asosiy_rasm',
                  'rasmlar', 'sevimli', 'yaratilgan']
        read_only_fields = ['holat', 'korilganlar', 'yaratilgan']

    def get_asosiy_rasm(self, obj):
        asosiy = obj.rasmlar.filter(asosiy=True).first()
        if asosiy:
            request = self.context.get('request')
            return request.build_absolute_uri(asosiy.rasm.url)
        return None

    def get_sevimli(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Sevimli.objects.filter(foydalanuvchi=request.user, mashina=obj).exists()
        return False


class MashinaYaratishSerializer(serializers.ModelSerializer):
    rasmlar = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Mashina
        fields = ['marka', 'model', 'yil', 'narx', 'probeg', 'ahvol', 'rang', 'viloyat', 'tavsif', 'rasmlar']

    def create(self, validated_data):
        rasmlar = validated_data.pop('rasmlar')
        mashina = Mashina.objects.create(**validated_data)

        for idx, rasm in enumerate(rasmlar):
            MashinaRasm.objects.create(mashina=mashina, rasm=rasm, asosiy=(idx == 0))

        return mashina

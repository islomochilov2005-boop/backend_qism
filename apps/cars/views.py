from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Mashina, Sevimli
from .serializers import MashinaSerializer, MashinaYaratishSerializer
from .filters import MashinaFilter


class MashinaListView(generics.ListAPIView):
    queryset = Mashina.objects.filter(holat='FAOL')
    serializer_class = MashinaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MashinaFilter


class MashinaDetailView(generics.RetrieveAPIView):
    queryset = Mashina.objects.all()
    serializer_class = MashinaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.korilganlar += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MashinaYaratishView(generics.CreateAPIView):
    serializer_class = MashinaYaratishSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(foydalanuvchi=self.request.user, holat='KUTILMOQDA')


class MeningMashinalarimView(generics.ListAPIView):
    serializer_class = MashinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mashina.objects.filter(foydalanuvchi=self.request.user).exclude(holat='OCHIRILGAN')


class MashinaUpdateView(generics.UpdateAPIView):
    serializer_class = MashinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mashina.objects.filter(foydalanuvchi=self.request.user)


class MashinaDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mashina.objects.filter(foydalanuvchi=self.request.user)

    def perform_destroy(self, instance):
        instance.holat = 'OCHIRILGAN'
        instance.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sotilgan(request, pk):
    try:
        mashina = Mashina.objects.get(pk=pk, foydalanuvchi=request.user)
        mashina.holat = 'SOTILGAN'
        mashina.save()
        return Response({'xabar': 'Sotilgan deb belgilandi'})
    except Mashina.DoesNotExist:
        return Response({'xato': 'Topilmadi'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sevimli(request, pk):
    try:
        mashina = Mashina.objects.get(pk=pk)
        sev, yaratildi = Sevimli.objects.get_or_create(foydalanuvchi=request.user, mashina=mashina)

        if not yaratildi:
            sev.delete()
            return Response({'xabar': 'O\'chirildi', 'sevimli': False})

        return Response({'xabar': 'Qo\'shildi', 'sevimli': True})
    except Mashina.DoesNotExist:
        return Response({'xato': 'Topilmadi'}, status=404)


class SevimlilarView(generics.ListAPIView):
    serializer_class = MashinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sevimli_ids = Sevimli.objects.filter(foydalanuvchi=self.request.user).values_list('mashina_id', flat=True)
        return Mashina.objects.filter(id__in=sevimli_ids, holat='FAOL')

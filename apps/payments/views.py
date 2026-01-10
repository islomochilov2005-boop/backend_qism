from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Paket, Tolov
from .serializers import PaketSerializer, TolovSerializer, TolovYaratishSerializer
from apps.cars.models import Mashina


class PaketListView(generics.ListAPIView):
    queryset = Paket.objects.filter(faol=True)
    serializer_class = PaketSerializer
    permission_classes = [AllowAny]


class TolovListView(generics.ListAPIView):
    serializer_class = TolovSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tolov.objects.filter(foydalanuvchi=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tolov_yaratish(request):
    serializer = TolovYaratishSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        mashina = Mashina.objects.get(
            id=serializer.validated_data['mashina_id'],
            foydalanuvchi=request.user,
            holat='KUTILMOQDA'
        )
        paket = Paket.objects.get(id=serializer.validated_data['paket_id'], faol=True)

        tolov = Tolov.objects.create(
            foydalanuvchi=request.user,
            mashina=mashina,
            paket=paket,
            summa=paket.narx
        )

        return Response({
            'tolov_id': tolov.id,
            'summa': str(tolov.summa),
            'xabar': 'To\'lov yaratildi'
        }, status=status.HTTP_201_CREATED)

    except Mashina.DoesNotExist:
        return Response({'xato': 'Mashina topilmadi'}, status=404)
    except Paket.DoesNotExist:
        return Response({'xato': 'Paket topilmadi'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def click_callback(request):
    tolov_id = request.data.get('merchant_trans_id')
    click_trans_id = request.data.get('click_trans_id')

    try:
        tolov = Tolov.objects.get(id=tolov_id)
        tolov.holat = 'TOLANDI'
        tolov.click_trans_id = click_trans_id
        tolov.save()

        tolov.mashina.holat = 'FAOL'
        tolov.mashina.save()

        return Response({'error': 0, 'error_note': 'Success'})
    except Tolov.DoesNotExist:
        return Response({'error': -5, 'error_note': 'Tolov topilmadi'})

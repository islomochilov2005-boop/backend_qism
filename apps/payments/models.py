from django.db import models
from django.contrib.auth import get_user_model
from apps.cars.models import Mashina

User = get_user_model()

class Paket(models.Model):
    nomi = models.CharField(max_length=50)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    tavsif = models.TextField()
    faol = models.BooleanField(default=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nomi} - {self.narx} so'm"


class Tolov(models.Model):
    HOLAT = [
        ('KUTILMOQDA', 'Kutilmoqda'),
        ('TOLANDI', 'To\'landi'),
        ('BEKOR', 'Bekor'),
    ]

    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    mashina = models.ForeignKey(Mashina, on_delete=models.CASCADE)
    paket = models.ForeignKey(Paket, on_delete=models.SET_NULL, null=True)
    summa = models.DecimalField(max_digits=10, decimal_places=2)
    holat = models.CharField(max_length=15, choices=HOLAT, default='KUTILMOQDA')
    click_trans_id = models.CharField(max_length=255, null=True, blank=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-yaratilgan']

    def __str__(self):
        return f"To'lov {self.id} - {self.holat}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Mashina(models.Model):
    HOLAT = [
        ('KUTILMOQDA', 'To\'lov kutilmoqda'),
        ('FAOL', 'Faol'),
        ('SOTILGAN', 'Sotilgan'),
        ('OCHIRILGAN', 'O\'chirilgan'),
    ]

    AHVOL = [
        ('YANGI', 'Yangi'),
        ('ISHLATILGAN', 'Ishlatilgan'),
    ]

    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    yil = models.IntegerField()
    narx = models.DecimalField(max_digits=12, decimal_places=2)
    probeg = models.IntegerField()
    ahvol = models.CharField(max_length=15, choices=AHVOL)
    rang = models.CharField(max_length=30)
    viloyat = models.CharField(max_length=50)
    tavsif = models.TextField()
    holat = models.CharField(max_length=15, choices=HOLAT, default='KUTILMOQDA')
    korilganlar = models.IntegerField(default=0)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-yaratilgan']

    def __str__(self):
        return f"{self.marka} {self.model} {self.yil}"


class MashinaRasm(models.Model):
    mashina = models.ForeignKey(Mashina, on_delete=models.CASCADE, related_name='rasmlar')
    rasm = models.ImageField(upload_to='mashina_rasmlar/')
    asosiy = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mashina} rasmi"


class Sevimli(models.Model):
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    mashina = models.ForeignKey(Mashina, on_delete=models.CASCADE)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['foydalanuvchi', 'mashina']


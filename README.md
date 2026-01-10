# Avto Elon - Backend API

Avtomobil e'lonlari mobile ilovasi uchun Django REST API backend.

---

## 🚀 Tezkor Boshlash

### 1. Loyihani Yuklab Olish
```bash
git clone <repository-url>
cd backend
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 3. Paketlarni O'rnatish
```bash
pip install -r requirements.txt
```

### 4. Migratsiya
```bash
python manage.py migrate
```

### 5. Superuser Yaratish
```bash
python manage.py createsuperuser
```

### 6. Test Paketlar Qo'shish
```bash
python manage.py shell
```
```python
from apps.payments.models import Paket
Paket.objects.create(nomi="Standart", narx=10000, tavsif="Oddiy e'lon", faol=True)
Paket.objects.create(nomi="Premium", narx=20000, tavsif="3 kun yuqorida", faol=True)
Paket.objects.create(nomi="VIP", narx=30000, tavsif="7 kun yuqorida + rangli", faol=True)
exit()
```

### 7. Serverni Ishga Tushirish
```bash
python manage.py runserver
```

**Server:** http://127.0.0.1:8000

---

## 📚 API Dokumentatsiya

### Swagger UI
```
http://127.0.0.1:8000/swagger/
```
Barcha API endpoint'larni ko'rish va test qilish mumkin.

### Admin Panel
```
http://127.0.0.1:8000/admin/
```

---

## 🔑 Authentication

JWT (JSON Web Token) ishlatiladi.

### Token Olish
```
POST /api/auth/kirish/
```

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Token Ishlatish

Har bir request'da header qo'shing:
```
Authorization: Bearer <access_token>
```

---

## 📱 API Endpoint'lar

### 1️⃣ AUTENTIFIKATSIYA

| Method | Endpoint | Tavsif | Auth |
|--------|----------|--------|------|
| POST | `/api/auth/royxat/` | Ro'yxatdan o'tish | Yo'q |
| POST | `/api/auth/kirish/` | Kirish | Yo'q |
| POST | `/api/auth/token/yangilash/` | Token yangilash | Yo'q |
| GET | `/api/auth/profil/` | Profil ko'rish | Ha |
| PUT | `/api/auth/profil/` | Profil yangilash | Ha |

### 2️⃣ MASHINALAR

| Method | Endpoint | Tavsif | Auth |
|--------|----------|--------|------|
| GET | `/api/mashinalar/` | Barcha mashinalar | Yo'q |
| GET | `/api/mashinalar/{id}/` | Bitta mashina | Yo'q |
| POST | `/api/mashinalar/yaratish/` | Yangi e'lon | Ha |
| GET | `/api/mashinalar/mening/` | Mening e'lonlarim | Ha |
| PUT | `/api/mashinalar/{id}/yangilash/` | Yangilash | Ha |
| DELETE | `/api/mashinalar/{id}/ochirish/` | O'chirish | Ha |
| POST | `/api/mashinalar/{id}/sotilgan/` | Sotilgan belgilash | Ha |
| POST | `/api/mashinalar/{id}/sevimli/` | Sevimli qo'shish/o'chirish | Ha |
| GET | `/api/mashinalar/sevimlilar/` | Sevimlilar ro'yxati | Ha |

### 3️⃣ TO'LOVLAR

| Method | Endpoint | Tavsif | Auth |
|--------|----------|--------|------|
| GET | `/api/tolovlar/paketlar/` | Paketlar ro'yxati | Yo'q |
| POST | `/api/tolovlar/yaratish/` | To'lov yaratish | Ha |
| GET | `/api/tolovlar/mening/` | Mening to'lovlarim | Ha |

---

## 📝 API Misollar

### Ro'yxatdan O'tish
```bash
curl -X POST http://127.0.0.1:8000/api/auth/royxat/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@mail.com",
    "telefon": "+998901234567",
    "parol": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Mashinalar Ro'yxati (Filter bilan)
```bash
curl "http://127.0.0.1:8000/api/mashinalar/?marka=Toyota&narx_min=15000&narx_max=30000"
```

### Yangi E'lon Yaratish
```bash
curl -X POST http://127.0.0.1:8000/api/mashinalar/yaratish/ \
  -H "Authorization: Bearer <token>" \
  -F "marka=Toyota" \
  -F "model=Camry" \
  -F "yil=2020" \
  -F "narx=25000" \
  -F "probeg=45000" \
  -F "ahvol=ISHLATILGAN" \
  -F "rang=Oq" \
  -F "viloyat=Toshkent" \
  -F "tavsif=Juda yaxshi holatda" \
  -F "rasmlar=@photo1.jpg" \
  -F "rasmlar=@photo2.jpg"
```

---

## 🎯 Flutter Integratsiya

### 1. Paketlar
```yaml
dependencies:
  http: ^1.1.0
  shared_preferences: ^2.2.2
```

### 2. API Service
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';
  String? _token;

  // Kirish
  Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/kirish/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _token = data['access'];
        return true;
      }
      return false;
    } catch (e) {
      print('Login error: $e');
      return false;
    }
  }

  // Mashinalar olish
  Future<List<dynamic>> getMashinalar({
    String? marka,
    int? narxMin,
    int? narxMax,
    int page = 1,
  }) async {
    String url = '$baseUrl/api/mashinalar/?page=$page';
    if (marka != null) url += '&marka=$marka';
    if (narxMin != null) url += '&narx_min=$narxMin';
    if (narxMax != null) url += '&narx_max=$narxMax';

    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['results'];
    }
    return [];
  }

  // Bitta mashina
  Future<Map<String, dynamic>?> getMashina(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/mashinalar/$id/'),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  // E'lon yaratish
  Future<bool> createMashina(Map<String, dynamic> data, List<String> imagePaths) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/mashinalar/yaratish/'),
    );

    request.headers['Authorization'] = 'Bearer $_token';
    
    // Ma'lumotlar
    request.fields['marka'] = data['marka'];
    request.fields['model'] = data['model'];
    request.fields['yil'] = data['yil'].toString();
    request.fields['narx'] = data['narx'].toString();
    request.fields['probeg'] = data['probeg'].toString();
    request.fields['ahvol'] = data['ahvol'];
    request.fields['rang'] = data['rang'];
    request.fields['viloyat'] = data['viloyat'];
    request.fields['tavsif'] = data['tavsif'];

    // Rasmlar
    for (var path in imagePaths) {
      request.files.add(await http.MultipartFile.fromPath('rasmlar', path));
    }

    var response = await request.send();
    return response.statusCode == 201;
  }

  // Sevimli qo'shish/o'chirish
  Future<bool> toggleFavorite(int id) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/mashinalar/$id/sevimli/'),
      headers: {'Authorization': 'Bearer $_token'},
    );

    return response.statusCode == 200 || response.statusCode == 201;
  }
}
```

### 3. Ishlatish
```dart
final api = ApiService();

// Login
await api.login('username', 'password');

// Mashinalarni olish
final mashinalar = await api.getMashinalar(
  marka: 'Toyota',
  narxMin: 15000,
  narxMax: 30000,
);

// E'lon yaratish
await api.createMashina({
  'marka': 'Toyota',
  'model': 'Camry',
  'yil': 2020,
  'narx': 25000,
  'probeg': 45000,
  'ahvol': 'ISHLATILGAN',
  'rang': 'Oq',
  'viloyat': 'Toshkent',
  'tavsif': 'Juda yaxshi holatda',
}, ['/path/to/image1.jpg', '/path/to/image2.jpg']);
```

---

## 🔍 Filter Parametrlari

Mashinalar ro'yxatida quyidagi filterlarni ishlatish mumkin:

- `marka` - Marka nomi (masalan: Toyota, Chevrolet)
- `model` - Model nomi (masalan: Camry, Nexia)
- `yil_min` - Minimal yil (masalan: 2015)
- `yil_max` - Maksimal yil (masalan: 2023)
- `narx_min` - Minimal narx (masalan: 10000)
- `narx_max` - Maksimal narx (masalan: 50000)
- `ahvol` - YANGI yoki ISHLATILGAN
- `viloyat` - Viloyat nomi (masalan: Toshkent, Samarqand)
- `page` - Sahifa raqami (1, 2, 3...)
- `page_size` - Har sahifada nechta (10, 20, 50)

**Misol:**
```
/api/mashinalar/?marka=Toyota&yil_min=2018&narx_max=30000&page=1
```

---

## 📊 Response Formatlari

### Muvaffaqiyatli Response
```json
{
  "count": 150,
  "next": "http://127.0.0.1:8000/api/mashinalar/?page=2",
  "previous": null,
  "results": [...]
}
```

### Xato Response
```json
{
  "detail": "Xato matni"
}
```

### Validation Xatolar
```json
{
  "username": ["Bu username band"],
  "email": ["Email noto'g'ri formatda"]
}
```

---

## 🛡️ Status Codes

- `200` - Muvaffaqiyatli
- `201` - Yaratildi
- `204` - No Content (o'chirildi)
- `400` - Noto'g'ri ma'lumot
- `401` - Autentifikatsiya kerak
- `403` - Ruxsat yo'q
- `404` - Topilmadi
- `500` - Server xatosi

---

## 🗂️ Loyiha Strukturasi

```
backend/
├── apps/
│   ├── users/          # Foydalanuvchilar
│   ├── cars/           # Mashinalar
│   ├── payments/       # To'lovlar
│   └── core/           # Umumiy funksiyalar
├── config/
│   ├── settings.py     # Sozlamalar
│   └── urls.py         # URL routing
├── media/              # Yuklangan rasmlar
├── db.sqlite3          # Ma'lumotlar bazasi
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📞 Yordam

Savol yoki muammolar bo'lsa:
- Swagger: http://127.0.0.1:8000/swagger/
- Admin: http://127.0.0.1:8000/admin/

---

## ✅ Tayyor!

Backend to'liq ishga tushirilgan va Flutter integratsiyasi uchun tayyor!

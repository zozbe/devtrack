# 🚀 DevTrack API - Clean Architecture ile Görev Takip Sistemi

DevTrack API, yazılım geliştirme ekiplerinin görevlerini yönetebilmesi için geliştirilmiş bir backend uygulamasıdır.

Proje, **FastAPI** kullanılarak geliştirilmiş olup **Clean Architecture**, **Repository Pattern** ve **Katmanlı Mimari** prensipleri uygulanarak tasarlanmıştır.

Bu proje sayesinde iş kuralları, veri erişim katmanı ve sunum katmanı birbirinden ayrılmıştır. Böylece sistem daha sürdürülebilir, test edilebilir ve ölçeklenebilir hale gelmiştir.

---

## 🎯 Projenin Amacı

Bu proje oluşturulurken temel hedefler:

* Clean Architecture mantığını uygulamak
* Katmanlar arası bağımlılıkları azaltmak
* FastAPI ile kurumsal proje yapısını deneyimlemek
* Repository Pattern kullanımını öğrenmek
* SOLID prensiplerine uygun geliştirme yapmak

---

## 🏗️ Mimari Yapı

```text
devtrack-api/
│
├── api/
│   ├── routes.py
│   └── schemas.py
│
├── application/
│   └── issue_service.py
│
├── domain/
│   └── issue.py
│
├── infrastructure/
│   └── issue_repository.py
│
└── main.py
```

### Domain Layer

Uygulamanın çekirdeğidir.

* Entity'ler
* Enum'lar
* İş kuralları

Bu katman herhangi bir framework bağımlılığı içermez.

### Application Layer

İş mantığının çalıştığı katmandır.

* Use Case'ler
* Servisler
* İş akışları

### Infrastructure Layer

Dış dünya ile iletişimi sağlar.

* Repository implementasyonları
* Veritabanı işlemleri
* Harici servis entegrasyonları

### API Layer

Kullanıcının sisteme giriş yaptığı katmandır.

* FastAPI endpointleri
* Request/Response modelleri
* Doğrulama işlemleri

---

## 🛠️ Kullanılan Teknolojiler

* Python 3.12+
* FastAPI
* Pydantic
* Uvicorn
* Clean Architecture
* Repository Pattern

---

## ⚙️ Kurulum

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/kullaniciadi/devtrack-api.git
cd devtrack-api
```

### 2. Sanal Ortam Oluşturun

```bash
python -m venv venv
```

### 3. Sanal Ortamı Aktifleştirin

Windows:

```bash
venv\Scripts\activate
```

Linux / MacOS:

```bash
source venv/bin/activate
```

### 4. Bağımlılıkları Kurun

```bash
pip install fastapi uvicorn pydantic
```

### 5. Uygulamayı Çalıştırın

```bash
uvicorn main:app --reload
```

---

## 🌐 Swagger Dokümantasyonu

Uygulama çalıştıktan sonra:

```text
http://127.0.0.1:8000/docs
```

adresinden Swagger UI üzerinden tüm endpointleri test edebilirsiniz.

---

## 📌 API Endpointleri

| Method | Endpoint     | Açıklama                     |
| ------ | ------------ | ---------------------------- |
| POST   | /issues      | Yeni görev oluşturur         |
| GET    | /issues      | Tüm görevleri listeler       |
| GET    | /issues/{id} | Görev detayını getirir       |
| PUT    | /issues/{id} | Görevi günceller             |
| GET    | /health      | Sistem durumunu kontrol eder |

---

## 📖 Öğrenilen Kavramlar

Bu proje kapsamında aşağıdaki yazılım mimarisi kavramları uygulanmıştır:

* Clean Architecture
* Dependency Direction
* Separation of Concerns
* Repository Pattern
* DTO (Data Transfer Object)
* Service Layer Pattern
* RESTful API Design

---

## 👨‍💻 Geliştirici

**Berfin Zozan İnanç**

Bilgisayar Mühendisi • Backend Geliştirme • Yazılım Mimarileri • FastAPI

Geliştirici Günlüğü
Bu projenin adım adım yapım aşamalarını ve mimari kararlarını Medium üzerinden paylaşıyorum.
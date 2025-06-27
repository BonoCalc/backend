# 📈 CreatiLink – Backend de Valoración de Bonos

Este proyecto es una API RESTful desarrollada en **FastAPI** con arquitectura **MVC** para gestionar la creación y valoración financiera de bonos corporativos bajo el **método de amortización alemán**.

## 🚀 Características principales

- Registro e inicio de sesión de usuarios con autenticación JWT.
- Creación de bonos con soporte para:
  - Gracia total y parcial
  - Tasa efectiva o nominal
  - Capitalización, días base, prima de redención
- Generación de cronograma de pagos por bono.
- Valoración financiera completa:
  - **TCEA**, **TREA**, **TIR**, **Duración**, **Convexidad**, **Precio máximo**
- Exportación de valoraciones a **Excel (.xlsx)**.
- Base de datos PostgreSQL, integración con Docker.

---

## 🧱 Tecnologías utilizadas

- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **Docker + Docker Compose**
- **Passlib, python-jose** (seguridad)
- **openpyxl** (Excel export)

---

## 📦 Instalación local (modo desarrollo)

### 1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/bonos-backend.git
cd bonos-backend
```


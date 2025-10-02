# Sprint2
Entrega Sprint 2, proyecto de Django

## Descripción del Proyecto

Este es un proyecto básico de Django 5.2.7 con la estructura inicial configurada y lista para desarrollo.

## Estructura del Proyecto

```
Sprint2/
├── manage.py                    # Utilidad de línea de comandos de Django
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
├── db.sqlite3                   # Base de datos SQLite (no versionada)
├── sprint2_project/             # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # Enrutamiento de URLs
│   ├── asgi.py                  # Punto de entrada ASGI
│   └── wsgi.py                  # Punto de entrada WSGI
└── main_app/                    # Aplicación Django principal
    ├── __init__.py
    ├── admin.py                 # Configuración del admin
    ├── apps.py                  # Configuración de la app
    ├── models.py                # Modelos de base de datos
    ├── views.py                 # Vistas
    ├── tests.py                 # Pruebas unitarias
    └── migrations/              # Migraciones de base de datos
```

## Requisitos

- Python 3.12+
- Django 5.2.7

## Instalación y Configuración

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

3. **Crear superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

5. **Acceder a la aplicación:**
   - Aplicación: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

## Comandos Útiles

- Verificar la configuración: `python manage.py check`
- Crear nueva aplicación: `python manage.py startapp nombre_app`
- Crear migraciones: `python manage.py makemigrations`
- Aplicar migraciones: `python manage.py migrate`
- Ejecutar tests: `python manage.py test`

## Estado del Proyecto

✓ Proyecto Django creado y configurado
✓ Base de datos SQLite inicializada
✓ Aplicación principal (main_app) creada
✓ Configuración de .gitignore aplicada
✓ Sistema de migraciones ejecutado

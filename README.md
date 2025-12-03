# Para ejecución:
1. Cambiar las direcciones de pedidos y productos en el kong
2. Para el despliegue de pedidos primero "sudo rm -rf /labs/Sprint2/venv" luego en /pedidos "python3 -m venv venv", seguido de "source venv/bin/activate", para finalizar con "python -m pip install --upgrade pip
python -m pip install -r pedidos/requirements.txt".
3. Una vez esto se procede a ejecutar pedidos con python3 main.py
4. Cambiar en el lógic de pedidos la url por la url del kong (cambiar solo la ip)
5. Para ejecutar pedidos en su microservicio, se debe hacer un npm install y seguido de ello un npm run dev (saldrá error pero ya estará corriendo).
   


# Sprint 2 – Provesi (Django)

Aplicación web en Django para gestionar productos y pedidos (crear, listar y despachar), con un pequeño reporte de los productos más vendidos en los últimos 90 días y un endpoint de health-check.

El proyecto contiene una app llamada `pedidos` y el proyecto base `provesi`.

## Características principales

- Gestión de productos (`Producto`): nombre, precio y stock.
- Gestión de pedidos (`Pedido`): cliente, producto, cantidad, estado y fecha del pedido.
- Despacho seguro de pedidos con transacciones y `select_for_update` para evitar condiciones de carrera y actualizar stock correctamente.
- Reporte simple de “top productos” de los últimos 90 días.
- Panel de administración de Django configurado.
- Endpoint de salud: `/health-check/`.

## Requisitos

- Python 3.9+
- pip (o gestor equivalente)
- (Opcional) Entorno virtual: `venv`, `virtualenv`, conda, etc.

Dependencias principales (ver `requirements.txt`):
- Django==4.2.25
- asgiref==3.9.2
- sqlparse==0.5.3
- typing_extensions==4.15.0

## Estructura del proyecto (resumen)

```
Sprint2/
├─ manage.py
├─ requirements.txt
├─ Dockerfile
├─ populate.py
├─ provesi/
│  ├─ settings.py
│  ├─ urls.py
│  └─ views.py
└─ pedidos/
	 ├─ models.py
	 ├─ views.py
	 ├─ urls.py
	 ├─ admin.py
	 ├─ migrations/
	 └─ templates/pedidos/
```

## Instalación y configuración

1) Clonar el repositorio y entrar a la carpeta del proyecto:

```bash
git clone <URL_DEL_REPO>
cd Sprint2
```

2) (Opcional pero recomendado) Crear y activar un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows PowerShell
```

3) Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

4) Revisar que la app esté registrada en `INSTALLED_APPS` (archivo `provesi/settings.py`):

```python
INSTALLED_APPS = [
		# ...
		'pedidos',  # o 'pedidos.apps.PedidosConfig'
]
```

5) Aplicar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Cargar datos de ejemplo (opcional)

El script `populate.py` genera productos y crea ~5000 pedidos en lotes.

```bash
python populate.py
```

Notas:
- El script usa creación en bulk para rendimiento.
- Si ya existen datos, puedes ajustar el script (tiene líneas comentadas para borrar previamente).

## Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

URL por defecto: http://127.0.0.1:8000/

## Endpoints principales

- `GET /` – Página de inicio del proyecto (`provesi.views.index`).
- `GET /health-check/` – Endpoint de salud (responde `ok`).
- `GET /pedidos/` – Lista de pedidos.
- `POST /pedidos/<id>/despachar/` – Despacha un pedido (actualiza estado y descuenta stock).
	- Respuesta JSON con éxito/error.
	- Nota: el endpoint está marcado con `@csrf_exempt` para facilitar pruebas. En producción, añadir CSRF.
- `GET /pedidos/reporte/` – Reporte de productos más vendidos en ~90 días.

## Panel de administración

Registra modelos `Producto` y `Pedido` con opciones de filtros y búsqueda.

1) Crear un superusuario:

```bash
python manage.py createsuperuser
```

2) Acceder a http://127.0.0.1:8000/admin/

## Pruebas

Si tienes pruebas unitarias en `pedidos/tests.py`:

```bash
python manage.py test
```

## Docker (opcional)

Se incluye un `Dockerfile`. Ejemplo básico de uso:

```bash
# Construir imagen
docker build -t sprint2-provesi:latest .

# Ejecutar contenedor (migraciones podrían ejecutarse en un entrypoint propio según tu preferencia)
docker run -p 8000:8000 sprint2-provesi:latest
```

Adapta el Dockerfile/entrypoint para aplicar migraciones automáticamente si lo deseas.

## Notas técnicas

- El despacho usa `transaction.atomic()` y `select_for_update()` para evitar despachos simultáneos inconsistentes.
- El campo `fecha_pedido` se crea con `default=timezone.now` para facilitar migraciones en bases con datos preexistentes.
- Plantillas ubicadas en `pedidos/templates/pedidos/`.

## Solución de problemas (FAQ)

- “No module named 'django'” al ejecutar `manage.py`:
	- Asegúrate de activar tu entorno virtual y de instalar `requirements.txt`.
- Error al migrar por `auto_now_add` pidiendo “one-off default”:
	- Ya está resuelto usando `default=timezone.now` en el modelo `Pedido`.
- Conflicto en rutas de `pedidos` (`''` duplicado):
	- Se ha dejado una sola ruta base en `pedidos/urls.py`.
- ¿Uso `'pedidos'` o `'pedidos.apps.PedidosConfig'`?
	- En Django 4.2 puedes usar `'pedidos'` y se autodetecta el AppConfig. La forma explícita también es válida; usa solo una.

---

© 2025 – Proyecto académico Sprint 2 (Django).

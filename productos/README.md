# 📦 Microservicio de Productos

Microservicio desarrollado en **Node.js + Express + MongoDB** para la gestión de productos de EPPs (Elementos de Protección Personal).

## 🚀 Stack Tecnológico

- **Runtime:** Node.js 18+
- **Framework:** Express.js
- **Base de Datos:** MongoDB
- **ODM:** Mongoose
- **Validación:** Express Validator

## 📁 Estructura del Proyecto

```
productos/
├── src/
│   ├── config/
│   │   └── database.js          # Configuración de MongoDB
│   ├── models/
│   │   └── Producto.js          # Modelo de Producto
│   ├── routes/
│   │   └── productos.routes.js  # Rutas de la API
│   ├── controllers/
│   │   └── productos.controller.js  # Lógica de negocio
│   └── app.js                   # Aplicación principal
├── .env                         # Variables de entorno
├── .gitignore
├── package.json
├── Dockerfile
└── README.md
```

## 🔧 Instalación y Configuración

### 1. Instalar dependencias

```bash
npm install
```

### 2. Configurar variables de entorno

Crea un archivo `.env` con:

```env
PORT=8080
MONGODB_URI=mongodb://monitoring_user:isis2503@localhost:27017/productos_db?authSource=admin
NODE_ENV=production
```

### 3. Ejecutar el servidor

**Modo desarrollo:**
```bash
npm run dev
```

**Modo producción:**
```bash
npm start
```

## 🌐 Endpoints de la API

### Health Check
- `GET /` - Información del microservicio
- `GET /health` - Estado del servicio

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos` | Obtener todos los productos |
| GET | `/productos/:id` | Obtener producto por ID |
| GET | `/productos/sku/:sku` | Obtener producto por SKU |
| GET | `/productos/categoria/:categoria` | Obtener productos por categoría |
| POST | `/productos` | Crear un producto |
| POST | `/productos/bulk` | Crear múltiples productos |
| PUT | `/productos/:id` | Actualizar un producto |
| DELETE | `/productos/:id` | Eliminar un producto |

## 📝 Categorías de Productos

- PROTECCIÓN MANUAL
- PROTECCIÓN AUDITIVA
- PROTECCIÓN VISUAL
- PROTECCIÓN RESPIRATORIA
- PROTECCIÓN FACIAL Y CABEZA
- PROTECCIÓN CORPORAL
- SEÑALIZACIÓN
- PROTECCIÓN ALTURAS
- PROTECCIÓN PIES
- ATENCIÓN PRIMEROS AUXILIOS
- PROTECCIÓN ESPACIOS CONFINADOS
- MATERIAL ATENCIÓN DERRAMES
- HERRAMIENTAS Y EQUIPOS
- OTROS
- TECNOLOGÍA

## 🐳 Docker

### Construir imagen
```bash
docker build -t productos-microservice .
```

### Ejecutar contenedor
```bash
docker run -p 8080:8080 --env-file .env productos-microservice
```

## 📦 Ejemplo de Producto

```json
{
  "SKU": "EPP-GNT-001",
  "descripcion": "Guantes de nitrilo azul, resistentes a químicos",
  "referencia": "NITRILO-2024",
  "peso": 0.12,
  "categoria": "PROTECCIÓN MANUAL"
}
```

## 🔗 Integración con Microservicio de Pedidos

Este microservicio se comunica con el microservicio de Pedidos vía HTTP. Los pedidos referencian productos usando el campo `productos` que contiene una lista de IDs de productos.

## 👨‍💻 Autor

Desarrollado para el proyecto Sprint 2 - Arquitectura de Microservicios
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { connectDB } = require('./config/database');
const productosRoutes = require('./routes/productos.routes');

// Crear aplicación Express
const app = express();

// Conectar a la base de datos
connectDB();

// Middlewares de seguridad
app.use(helmet()); // Agrega headers de seguridad
app.use(cors());
app.use(express.json({ limit: '10mb' })); // Limitar tamaño del body
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logger middleware simple
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path} - ${new Date().toISOString()}`);
  next();
});

// Middleware para prevenir NoSQL injection adicional
app.use((req, res, next) => {
  // Limpiar query params de operadores peligrosos
  if (req.query) {
    Object.keys(req.query).forEach(key => {
      if (typeof req.query[key] === 'string') {
        req.query[key] = req.query[key].replace(/[${}]/g, '');
      }
    });
  }
  next();
});

// Ruta de health check
app.get('/', (req, res) => {
  res.json({
    message: '🚀 Microservicio de Productos - Node.js + Express + PostgreSQL',
    status: 'active',
    database: 'PostgreSQL',
    security: 'SQL Injection Protected',
    timestamp: new Date().toISOString(),
    endpoints: {
      productos: '/productos',
      health: '/health'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Rutas de la API
app.use('/productos', productosRoutes);

// Manejador de rutas no encontradas
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Ruta no encontrada'
  });
});

// Manejador de errores global
app.use((err, req, res, next) => {
  console.error('Error:', err.stack);
  res.status(500).json({
    success: false,
    error: 'Error interno del servidor'
  });
});

// Puerto del servidor
const PORT = process.env.PORT || 8080;

// Iniciar servidor
app.listen(PORT, '0.0.0.0', () => {
  console.log(`
  ╔════════════════════════════════════════════════════╗
  ║                                                    ║
  ║   🚀 Microservicio de Productos                   ║
  ║                                                    ║
  ║   📦 Stack: Node.js + Express + PostgreSQL        ║
  ║   🔒 Seguridad: SQL Injection Protected           ║
  ║   🌐 Puerto: ${PORT}                                   ║
  ║   🔧 Ambiente: ${process.env.NODE_ENV}                    ║
  ║                                                    ║
  ╚════════════════════════════════════════════════════╝
  `);
});
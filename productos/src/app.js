require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/database');
const productosRoutes = require('./routes/productos.routes');

// Crear aplicación Express
const app = express();

// Conectar a la base de datos
connectDB();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logger middleware simple
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path} - ${new Date().toISOString()}`);
  next();
});

// Ruta de health check
app.get('/', (req, res) => {
  res.json({
    message: '🚀 Microservicio de Productos - Node.js + Express + MongoDB',
    status: 'active',
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
  ║   📦 Stack: Node.js + Express + MongoDB           ║
  ║   🌐 Puerto: ${PORT}                                   ║
  ║   🔧 Ambiente: ${process.env.NODE_ENV}                    ║
  ║                                                    ║
  ╚════════════════════════════════════════════════════╝
  `);
});
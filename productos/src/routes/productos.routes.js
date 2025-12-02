const express = require('express');
const router = express.Router();
const {
  crearProducto,
  obtenerProductos,
  obtenerProductoPorId,
  obtenerProductoPorSKU,
  actualizarProducto,
  eliminarProducto,
  crearProductosBulk,
  obtenerProductosPorCategoria
} = require('../controllers/productos.controller');

// Rutas principales
router.route('/')
  .get(obtenerProductos)
  .post(crearProducto);

// Crear múltiples productos
router.post('/bulk', crearProductosBulk);

// Obtener por SKU
router.get('/sku/:sku', obtenerProductoPorSKU);

// Obtener por categoría
router.get('/categoria/:categoria', obtenerProductosPorCategoria);

// Rutas con ID
router.route('/:id')
  .get(obtenerProductoPorId)
  .put(actualizarProducto)
  .delete(eliminarProducto);

module.exports = router;
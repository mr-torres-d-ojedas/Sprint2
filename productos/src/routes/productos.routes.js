const express = require('express');
const router = express.Router();
const { body, param } = require('express-validator');
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

// Validaciones para crear/actualizar producto
const validacionProducto = [
  body('SKU')
    .optional()
    .trim()
    .isLength({ max: 100 })
    .withMessage('SKU debe tener máximo 100 caracteres')
    .matches(/^[a-zA-Z0-9\-_]*$/)
    .withMessage('SKU solo puede contener letras, números, guiones y guiones bajos'),
  
  body('descripcion')
    .optional()
    .trim()
    .isLength({ max: 250 })
    .withMessage('Descripción debe tener máximo 250 caracteres')
    .escape(), // Escapa caracteres HTML peligrosos
  
  body('referencia')
    .optional()
    .trim()
    .isLength({ max: 150 })
    .withMessage('Referencia debe tener máximo 150 caracteres')
    .escape(),
  
  body('peso')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('El peso debe ser un número positivo'),
  
  body('precio')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('El precio debe ser un número positivo'),
  
  body('categoria')
    .optional()
    .isIn([
      'PROTECCIÓN MANUAL',
      'PROTECCIÓN AUDITIVA',
      'PROTECCIÓN VISUAL',
      'PROTECCIÓN RESPIRATORIA',
      'PROTECCIÓN FACIAL Y CABEZA',
      'PROTECCIÓN CORPORAL',
      'SEÑALIZACIÓN',
      'PROTECCIÓN ALTURAS',
      'PROTECCIÓN PIES',
      'ATENCIÓN PRIMEROS AUXILIOS',
      'PROTECCIÓN ESPACIOS CONFINADOS',
      'MATERIAL ATENCIÓN DERRAMES',
      'HERRAMIENTAS Y EQUIPOS',
      'OTROS',
      'TECNOLOGÍA'
    ])
    .withMessage('Categoría no válida')
];

// Validación para UUID
const validacionUUID = [
  param('id')
    .isUUID()
    .withMessage('ID debe ser un UUID válido')
];

// Rutas principales
router.route('/')
  .get(obtenerProductos)
  .post(validacionProducto, crearProducto);

// Crear múltiples productos
router.post('/bulk', crearProductosBulk);

// Obtener por SKU (sanitizado en el controller)
router.get('/sku/:sku', obtenerProductoPorSKU);

// Obtener por categoría
router.get('/categoria/:categoria', obtenerProductosPorCategoria);

// Rutas con ID
router.route('/:id')
  .get(validacionUUID, obtenerProductoPorId)
  .put([...validacionUUID, ...validacionProducto], actualizarProducto)
  .delete(validacionUUID, eliminarProducto);

module.exports = router;
const Producto = require('../models/Producto');
const { Op } = require('sequelize');
const { validationResult } = require('express-validator');

// Función auxiliar para sanitizar búsquedas
const sanitizeSearchTerm = (term) => {
  if (!term) return term;
  // Remover caracteres peligrosos para SQL
  return term.replace(/['";\\]/g, '').trim();
};

// @desc    Crear un nuevo producto
// @route   POST /productos
// @access  Public
const crearProducto = async (req, res) => {
  try {
    // Validar errores de express-validator
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const producto = await Producto.create(req.body);
    
    res.status(201).json({
      success: true,
      data: producto
    });
  } catch (error) {
    console.error('Error al crear producto:', error);
    
    // Error de validación de Sequelize
    if (error.name === 'SequelizeValidationError') {
      return res.status(400).json({
        success: false,
        error: 'Datos de producto inválidos',
        details: error.errors.map(e => e.message)
      });
    }
    
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
};

// @desc    Obtener todos los productos
// @route   GET /productos
// @access  Public
const obtenerProductos = async (req, res) => {
  try {
    const productos = await Producto.findAll({
      order: [['createdAt', 'DESC']]
    });
    
    res.status(200).json({
      success: true,
      count: productos.length,
      data: productos
    });
  } catch (error) {
    console.error('Error al obtener productos:', error);
    res.status(500).json({
      success: false,
      error: 'Error al obtener productos'
    });
  }
};

// @desc    Obtener un producto por ID
// @route   GET /productos/:id
// @access  Public
const obtenerProductoPorId = async (req, res) => {
  try {
    const producto = await Producto.findByPk(req.params.id);
    
    if (!producto) {
      return res.status(404).json({
        success: false,
        error: 'Producto no encontrado'
      });
    }
    
    res.status(200).json({
      success: true,
      data: producto
    });
  } catch (error) {
    console.error('Error al obtener producto:', error);
    res.status(500).json({
      success: false,
      error: 'Error al obtener producto'
    });
  }
};

// @desc    Obtener un producto por SKU
// @route   GET /productos/sku/:sku
// @access  Public
const obtenerProductoPorSKU = async (req, res) => {
  try {
    const skuSanitizado = sanitizeSearchTerm(req.params.sku);
    
    const producto = await Producto.findOne({
      where: { SKU: skuSanitizado }
    });
    
    if (!producto) {
      return res.status(404).json({
        success: false,
        error: 'Producto no encontrado'
      });
    }
    
    res.status(200).json({
      success: true,
      data: producto
    });
  } catch (error) {
    console.error('Error al obtener producto por SKU:', error);
    res.status(500).json({
      success: false,
      error: 'Error al obtener producto'
    });
  }
};

// @desc    Actualizar un producto
// @route   PUT /productos/:id
// @access  Public
const actualizarProducto = async (req, res) => {
  try {
    // Validar errores de express-validator
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        errors: errors.array()
      });
    }

    const producto = await Producto.findByPk(req.params.id);
    
    if (!producto) {
      return res.status(404).json({
        success: false,
        error: 'Producto no encontrado'
      });
    }
    
    await producto.update(req.body);
    
    res.status(200).json({
      success: true,
      data: producto
    });
  } catch (error) {
    console.error('Error al actualizar producto:', error);
    
    if (error.name === 'SequelizeValidationError') {
      return res.status(400).json({
        success: false,
        error: 'Datos de producto inválidos',
        details: error.errors.map(e => e.message)
      });
    }
    
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
};

// @desc    Eliminar un producto
// @route   DELETE /productos/:id
// @access  Public
const eliminarProducto = async (req, res) => {
  try {
    const producto = await Producto.findByPk(req.params.id);
    
    if (!producto) {
      return res.status(404).json({
        success: false,
        error: 'Producto no encontrado'
      });
    }
    
    await producto.destroy();
    
    res.status(200).json({
      success: true,
      data: {},
      message: 'Producto eliminado correctamente'
    });
  } catch (error) {
    console.error('Error al eliminar producto:', error);
    res.status(500).json({
      success: false,
      error: 'Error al eliminar producto'
    });
  }
};

// @desc    Crear múltiples productos (bulk)
// @route   POST /productos/bulk
// @access  Public
const crearProductosBulk = async (req, res) => {
  try {
    if (!Array.isArray(req.body)) {
      return res.status(400).json({
        success: false,
        error: 'El body debe ser un array de productos'
      });
    }
    
    const productos = await Producto.bulkCreate(req.body, {
      validate: true
    });
    
    res.status(201).json({
      success: true,
      count: productos.length,
      data: productos
    });
  } catch (error) {
    console.error('Error al crear productos en bulk:', error);
    
    if (error.name === 'SequelizeValidationError') {
      return res.status(400).json({
        success: false,
        error: 'Datos de productos inválidos',
        details: error.errors.map(e => e.message)
      });
    }
    
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
};

// @desc    Obtener productos por categoría
// @route   GET /productos/categoria/:categoria
// @access  Public
const obtenerProductosPorCategoria = async (req, res) => {
  try {
    const categoriaSanitizada = sanitizeSearchTerm(req.params.categoria);
    
    const productos = await Producto.findAll({
      where: { categoria: categoriaSanitizada },
      order: [['createdAt', 'DESC']]
    });
    
    res.status(200).json({
      success: true,
      count: productos.length,
      data: productos
    });
  } catch (error) {
    console.error('Error al obtener productos por categoría:', error);
    res.status(500).json({
      success: false,
      error: 'Error al obtener productos'
    });
  }
};

module.exports = {
  crearProducto,
  obtenerProductos,
  obtenerProductoPorId,
  obtenerProductoPorSKU,
  actualizarProducto,
  eliminarProducto,
  crearProductosBulk,
  obtenerProductosPorCategoria
};
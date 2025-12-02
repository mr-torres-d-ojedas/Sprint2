const Producto = require('../models/Producto');

// @desc    Crear un nuevo producto
// @route   POST /productos
// @access  Public
const crearProducto = async (req, res) => {
  try {
    const producto = new Producto(req.body);
    const productoGuardado = await producto.save();
    
    res.status(201).json({
      success: true,
      data: productoGuardado
    });
  } catch (error) {
    console.error('Error al crear producto:', error);
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
    const productos = await Producto.find();
    
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
    const producto = await Producto.findById(req.params.id);
    
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
    const producto = await Producto.findOne({ SKU: req.params.sku });
    
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
    const producto = await Producto.findByIdAndUpdate(
      req.params.id,
      req.body,
      {
        new: true, // Devuelve el documento actualizado
        runValidators: true // Ejecuta las validaciones del schema
      }
    );
    
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
    console.error('Error al actualizar producto:', error);
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
    const producto = await Producto.findByIdAndDelete(req.params.id);
    
    if (!producto) {
      return res.status(404).json({
        success: false,
        error: 'Producto no encontrado'
      });
    }
    
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
    
    const productos = await Producto.insertMany(req.body);
    
    res.status(201).json({
      success: true,
      count: productos.length,
      data: productos
    });
  } catch (error) {
    console.error('Error al crear productos en bulk:', error);
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
    const productos = await Producto.find({ 
      categoria: req.params.categoria 
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
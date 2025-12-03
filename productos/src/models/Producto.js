const mongoose = require('mongoose');

// Enumeración de categorías
const CategoriasProducto = [
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
];

const ProductoSchema = new mongoose.Schema(
  {
    SKU: {
      type: String,
      required: false,
      trim: true,
      index: true
    },
    descripcion: {
      type: String,
      required: false,
      trim: true,
      maxlength: 250
    },
    referencia: {
      type: String,
      required: false,
      trim: true,
      maxlength: 150
    },
    peso: {
      type: Number,
      default: 0.0,
      min: 0
    },
    categoria: {
      type: String,
      enum: CategoriasProducto,
      default: 'OTROS'
    },
    precio: {
      type: Number,
      default: 0.0,
      min: 0
    }
  },
  {
    timestamps: true, // Agrega createdAt y updatedAt automáticamente
    versionKey: false
  }
);

// Índice para búsquedas por SKU
ProductoSchema.index({ SKU: 1 });

// Método para transformar el objeto al devolverlo
ProductoSchema.set('toJSON', {
  transform: (doc, ret) => {
    ret.id = ret._id;
    delete ret._id;
    return ret;
  }
});

module.exports = mongoose.model('Producto', ProductoSchema);
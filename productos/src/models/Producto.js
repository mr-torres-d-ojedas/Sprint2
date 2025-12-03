const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

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

const Producto = sequelize.define('Producto', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true,
    allowNull: false
  },
  SKU: {
    type: DataTypes.STRING(100),
    allowNull: true,
    validate: {
      len: {
        args: [0, 100],
        msg: 'SKU debe tener máximo 100 caracteres'
      },
      // Validación para evitar caracteres maliciosos
      is: {
        args: /^[a-zA-Z0-9\-_]*$/,
        msg: 'SKU solo puede contener letras, números, guiones y guiones bajos'
      }
    }
  },
  descripcion: {
    type: DataTypes.STRING(250),
    allowNull: true,
    validate: {
      len: {
        args: [0, 250],
        msg: 'Descripción debe tener máximo 250 caracteres'
      }
    }
  },
  referencia: {
    type: DataTypes.STRING(150),
    allowNull: true,
    validate: {
      len: {
        args: [0, 150],
        msg: 'Referencia debe tener máximo 150 caracteres'
      }
    }
  },
  peso: {
    type: DataTypes.FLOAT,
    defaultValue: 0.0,
    allowNull: false,
    validate: {
      min: {
        args: 0,
        msg: 'El peso no puede ser negativo'
      },
      isFloat: {
        msg: 'El peso debe ser un número decimal'
      }
    }
  },
  precio: {
    type: DataTypes.DECIMAL(10, 2),
    defaultValue: 0.00,
    allowNull: false,
    validate: {
      min: {
        args: 0,
        msg: 'El precio no puede ser negativo'
      },
      isDecimal: {
        msg: 'El precio debe ser un número decimal'
      }
    }
  },
  categoria: {
    type: DataTypes.ENUM(...CategoriasProducto),
    defaultValue: 'OTROS',
    allowNull: false,
    validate: {
      isIn: {
        args: [CategoriasProducto],
        msg: 'Categoría no válida'
      }
    }
  }
}, {
  tableName: 'productos',
  timestamps: true,
  
  // Hooks para sanitización adicional
  hooks: {
    beforeValidate: (producto, options) => {
      // Sanitizar strings: trim y remover caracteres peligrosos
      if (producto.SKU) {
        producto.SKU = producto.SKU.trim();
      }
      if (producto.descripcion) {
        producto.descripcion = producto.descripcion.trim();
      }
      if (producto.referencia) {
        producto.referencia = producto.referencia.trim();
      }
    }
  },
  
  // Configuración de índices para mejorar rendimiento
  indexes: [
    {
      unique: false,
      fields: ['SKU']
    },
    {
      unique: false,
      fields: ['categoria']
    }
  ]
});

// Método para transformar a JSON
Producto.prototype.toJSON = function() {
  const values = Object.assign({}, this.get());
  return values;
};

module.exports = Producto;
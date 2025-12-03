const { Sequelize } = require('sequelize');

// Configuración de PostgreSQL con Sequelize
const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT || 5432,
    dialect: 'postgres',
    
    // Configuración de pool de conexiones
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    },
    
    // Logging
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    
    // Timezone
    timezone: '-05:00',
    
    // Configuraciones de seguridad
    dialectOptions: {
      ssl: process.env.DB_SSL === 'true' ? {
        require: true,
        rejectUnauthorized: false
      } : false
    }
  }
);

const connectDB = async () => {
  try {
    await sequelize.authenticate();
    console.log('✅ PostgreSQL Connected successfully');
    console.log(`📦 Database: ${process.env.DB_NAME}`);
    console.log(`🏠 Host: ${process.env.DB_HOST}`);
    
    // Sincronizar modelos (crear tablas si no existen)
    // alter: true actualiza las tablas sin borrar datos
    await sequelize.sync({ alter: true });
    console.log('✅ Database synchronized');
    
  } catch (error) {
    console.error('❌ Error connecting to PostgreSQL:', error.message);
    process.exit(1);
  }
};

module.exports = { sequelize, connectDB };
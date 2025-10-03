import os
import sys
import django
from decimal import Decimal
from random import choice, randint, uniform

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'provesi.settings')  # OJO proyecto
django.setup()

# Importar modelos
from pedidos.models import Producto, Pedido  # Cambia por tu app

def generar_productos_provesi():
    """Generar productos de Provesi - EPP y Seguridad Industrial"""
    
    # Productos por marcas que distribuye Provesi
    productos_3m = [
        "Mascarilla 3M 8210", "Respirador 3M 6200", "Casco 3M H-700", "Tapones 3M 1100",
        "Gafas 3M SecureFit", "Guantes 3M Comfort Grip", "Protector Auditivo 3M Peltor",
        "Filtro 3M 6001", "Mascarilla 3M 9210", "Arnés 3M DBI-SALA"
    ]
    
    productos_steelpro = [
        "Casco Steelpro Linesman", "Botas Steelpro Dieléctrica", "Guantes Steelpro Soldador",
        "Chaleco Steelpro Reflectivo", "Gafas Steelpro Clear", "Overol Steelpro Antifluido"
    ]
    
    productos_kimberly = [
        "Guantes Kimberly Nitrilo", "Bata Kimberly SMS", "Respirador Kimberly N95",
        "Toalla Industrial Kimberly", "Papel Higiénico Kimberly"
    ]
    
    productos_ansell = [
        "Guantes Ansell PowerFlex", "Guantes Ansell HyFlex", "Guantes Ansell TouchNTuff",
        "Guantes Ansell AlphaTec", "Guantes Ansell Versatouch"
    ]
    
    productos_croydon = [
        "Botas Croydon Dieléctrica", "Botas Croydon Punta Acero", "Botas Croydon Antideslizante",
        "Botas Croydon Impermeable"
    ]
    
    productos_generales = [
        # EPP General
        "Casco de Seguridad Blanco", "Casco de Seguridad Amarillo", "Casco de Seguridad Rojo",
        "Chaleco Reflectivo Amarillo", "Chaleco Reflectivo Naranja", "Arnés Cuerpo Completo",
        "Línea de Vida", "Mosquetón Acero", "Eslinga Poliéster", "Cuerda Estática",
        
        # Protección Respiratoria
        "Mascarilla Quirúrgica", "Respirador N95", "Filtro P100", "Media Cara Silicona",
        "Cara Completa Respirador", "Cartucho Químico", "Pre-filtro Algodón",
        
        # Protección Visual
        "Gafas Seguridad Transparente", "Gafas Seguridad Oscura", "Gafas Panorámicas",
        "Pantalla Facial", "Monogafas", "Protector Facial Policarbonato",
        
        # Protección Auditiva
        "Tapones Espuma", "Tapones Silicona", "Protector Copa", "Protector Inserción",
        
        # Calzado Seguridad
        "Botas Punta Acero Negro", "Botas Punta Acero Café", "Zapatos Seguridad",
        "Plantilla Acero", "Plantilla Kevlar", "Calcetines Trabajo",
        
        # Protección Manos
        "Guantes Carnaza", "Guantes Nitrilo", "Guantes Látex", "Guantes PVC",
        "Guantes Anticorte", "Guantes Soldador", "Guantes Químicos", "Guantes Térmicos",
        
        # Ropa de Trabajo
        "Overol Industrial", "Camisa Drill", "Pantalón Drill", "Delantal PVC",
        "Delantal Carnaza", "Bata Laboratorio", "Uniforme Médico", "Pijama Quirúrgica",
        
        # Herramientas
        "Martillo Garra", "Destornillador Plano", "Destornillador Phillips", "Alicate Universal",
        "Llave Inglesa", "Metro Metálico", "Nivel Burbuja", "Taladro Eléctrico",
        "Sierra Manual", "Lima Metálica", "Berbiquí", "Formón",
        
        # Equipos Computo
        "Laptop HP", "Desktop Dell", "Monitor Samsung 24", "Teclado Logitech",
        "Mouse Inalámbrico", "Impresora HP", "Router WiFi", "Switch 8 Puertos",
        "Disco Duro Externo", "Memoria USB 32GB", "Cable HDMI", "Webcam HD",
        
        # Electrodomésticos
        "Nevera 250L", "Lavadora 15Kg", "Microondas 1.2Cu", "Licuadora Industrial",
        "Cafetera 12 Tazas", "Plancha Vapor", "Ventilador Techo", "Aire Acondicionado",
        
        # Bioseguridad
        "Gel Antibacterial", "Alcohol Glicerinado", "Termómetro Digital", "Dispensador Gel",
        "Tapete Desinfectante", "Atomizador Manual", "Desinfectante Superficies",
        
        # Señalización
        "Señal Prohibido Fumar", "Señal Uso Obligatorio Casco", "Señal Salida Emergencia",
        "Cinta Peligro", "Conos Tráfico", "Valla Peatonal", "Extintor 10Lb"
    ]
    
    # Combinar todos los productos
    todos_productos = (productos_3m + productos_steelpro + productos_kimberly + 
                      productos_ansell + productos_croydon + productos_generales)
    
    productos_lista = []
    
    for nombre in todos_productos:
        precio = uniform(5000, 500000)  # Precios en pesos colombianos
        stock = randint(10, 1000)
        
        productos_lista.append(Producto(
            nombre=nombre,
            precio=Decimal(str(round(precio, 2))),
            stock=stock
        ))
    
    return productos_lista

def crear_pedidos_bulk(productos, cantidad_pedidos=5000):
    """Crear 5000 pedidos de forma eficiente"""
    
    nombres_clientes = [
        # Empresas colombianas típicas
        "Ecopetrol S.A.", "Grupo Nutresa", "Bancolombia", "Grupo Éxito", "ISA",
        "Cemex Colombia", "Bavaria S.A.", "Alpina", "Colpatria", "Avianca",
        "Mineros S.A.", "Cementos Argos", "EPM", "Gas Natural", "Claro Colombia",
        
        # Personas naturales
        "Carlos Rodríguez", "María García", "Juan López", "Ana Martínez", "Luis Hernández",
        "Carmen Díaz", "José González", "Laura Pérez", "Diego Ramírez", "Patricia Torres",
        "Fernando Ruiz", "Claudia Vargas", "Andrés Moreno", "Isabel Castro", "Roberto Silva",
        "Mónica Jiménez", "Pablo Guerrero", "Beatriz Mendoza", "Sergio Ortega", "Natalia Rojas",
        "Óscar Delgado", "Cristina Vega", "Javier Flores", "Lucía Herrera", "Manuel Aguilar",
        "Raquel Navarro", "Alberto Sánchez", "Silvia Romero", "Eduardo Molina", "Paola Cruz"
    ]
    
    pedidos_lista = []
    estados = ['pendiente', 'despachado']
    
    print(f"Creando {cantidad_pedidos} pedidos...")
    
    for i in range(cantidad_pedidos):
        pedido = Pedido(
            cliente=choice(nombres_clientes),
            producto=choice(productos),
            cantidad=randint(1, 50),
            estado=choice(estados)
        )
        pedidos_lista.append(pedido)
        
        if (i + 1) % 1000 == 0:
            print(f"Generados {i + 1} pedidos...")
    
    return pedidos_lista

def main():
    print("🏭 PROVESI COLOMBIA - POBLANDO BASE DE DATOS")
    print("=" * 50)
    
    # Crear productos
    print("📦 Generando productos de EPP y Seguridad Industrial...")
    productos_lista = generar_productos_provesi()
    
    # Borrar productos existentes (opcional)
    # Producto.objects.all().delete()
    # Pedido.objects.all().delete()
    
    # Crear productos en bulk
    productos_creados = Producto.objects.bulk_create(productos_lista, ignore_conflicts=True)
    print(f"✅ {len(productos_creados)} productos creados")
    
    # Obtener todos los productos para crear pedidos
    todos_productos = list(Producto.objects.all())
    
    if not todos_productos:
        print("❌ No hay productos disponibles para crear pedidos")
        return
    
    # Crear pedidos en bulk
    print("📋 Generando 5000 pedidos...")
    pedidos_lista = crear_pedidos_bulk(todos_productos, 5000)
    
    # Crear pedidos en lotes para evitar problemas de memoria
    batch_size = 500
    total_creados = 0
    
    for i in range(0, len(pedidos_lista), batch_size):
        batch = pedidos_lista[i:i + batch_size]
        Pedido.objects.bulk_create(batch)
        total_creados += len(batch)
        print(f"📊 Creados {total_creados}/{len(pedidos_lista)} pedidos...")
    
    print("=" * 50)
    print("✅ ¡BASE DE DATOS POBLADA EXITOSAMENTE!")
    print(f"📦 Productos totales: {Producto.objects.count()}")
    print(f"📋 Pedidos totales: {Pedido.objects.count()}")
    print("🇨🇴 Provesi Colombia - EPP y Seguridad Industrial")

if __name__ == "__main__":
    main()	
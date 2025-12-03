# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para microservicio Productos (Node.js + Express + MongoDB)
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - msd-traffic-mongodb-productos (puerto 27017)
#    - msd-traffic-apps-productos (puerto 8080)
#    - msd-traffic-ssh-productos (puerto 22)
# 2. Instancias EC2:
#    - msd-productos-db (MongoDB instalado y configurado)
#    - msd-productos-ms (Servicio Node.js instalado y configurado)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.18.0"
    }
  }
}

# Variable. Define la región de AWS donde se desplegará la infraestructura.
variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

# Variable. Define el prefijo usado para nombrar los recursos en AWS.
variable "project_prefix" {
  description = "Prefix used for naming AWS resources"
  type        = string
  default     = "msd"
}

# Variable. Define el tipo de instancia EC2 a usar para las máquinas virtuales.
variable "instance_type" {
  description = "EC2 instance type for application hosts"
  type        = string
  default     = "t3.micro"
}

# Proveedor. Define el proveedor de infraestructura (AWS) y la región.
provider "aws" {
  region = var.region
}

# Variables locales usadas en la configuración de Terraform.
locals {
  project_name = "${var.project_prefix}-microservices"
  repository   = "https://github.com/mr-torres-d-ojedas/Sprint2.git"

  common_tags = {
    Project   = local.project_name
    ManagedBy = "Terraform"
  }
}

# Variable. AMI de Ubuntu 24.04 para us-east-1
# Si estás en otra región, busca el AMI correspondiente en:
# https://cloud-images.ubuntu.com/locator/ec2/
variable "ubuntu_ami" {
  description = "AMI ID for Ubuntu 24.04 LTS"
  type        = string
  default     = "ami-0e2c8caa4b6378d8c"  # Ubuntu 24.04 LTS en us-east-1
}

# Recurso. Define el grupo de seguridad para el tráfico de los microservicios (8080).
resource "aws_security_group" "traffic_apps_productos" {
    name        = "${var.project_prefix}-traffic-apps-productos"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-apps-productos"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico SSH (22) y permite todo el tráfico saliente.
resource "aws_security_group" "traffic_ssh_productos" {
  name        = "${var.project_prefix}-traffic-ssh-productos"
  description = "Allow SSH access"

  ingress {
    description = "SSH access from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-ssh-productos"
  })
}

# Recurso. Define el grupo de seguridad para el tráfico de MongoDB.
resource "aws_security_group" "traffic_mongodb_productos" {
    name        = "${var.project_prefix}-traffic-mongodb-productos"
    description = "Allow application traffic on port 27017"

    ingress {
        description = "MongoDB access for database layer"
        from_port   = 27017
        to_port     = 27017
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-mongodb-productos"
    })
}

# Recurso. Define la instancia EC2 para la base de datos de Productos (MongoDB).
resource "aws_instance" "productos_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_mongodb_productos.id, aws_security_group.traffic_ssh_productos.id]

  user_data = <<-EOT
              #!/bin/bash

              docker run -d --name productos-db -p 27017:27017 \
                            -e MONGO_INITDB_ROOT_USERNAME=monitoring_user \
                            -e MONGO_INITDB_ROOT_PASSWORD=isis2503 \
                            mongodb/mongodb-community-server
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-productos-db"
    Role = "productos-db"
  })
}

# Recurso. Define la instancia EC2 para el microservicio de Productos (Node.js).
resource "aws_instance" "productos_ms" {
  ami                         = var.ubuntu_ami
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_apps_productos.id, aws_security_group.traffic_ssh_productos.id]

  user_data = <<-EOT
              #!/bin/bash

              # Configurar variables de entorno
              sudo export PRODUCTOS_DB_HOST=${aws_instance.productos_db.private_ip}
              echo "PRODUCTOS_DB_HOST=${aws_instance.productos_db.private_ip}" | sudo tee -a /etc/environment

              # Actualizar sistema
              sudo apt-get update -y
              sudo apt-get install -y git curl

              # Instalar Node.js 18.x
              curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
              sudo apt-get install -y nodejs

              # Verificar instalación
              node --version
              npm --version

              # Crear directorio de trabajo
              mkdir -p /labs
              cd /labs

              # Clonar repositorio
              if [ ! -d Sprint2 ]; then
                git clone --branch microservicios --single-branch ${local.repository}
              fi
              
              cd Sprint2/productos

              # Crear archivo .env con la IP de la base de datos
              cat > .env << EOF
              PORT=8080
              MONGODB_URI=mongodb://monitoring_user:isis2503@${aws_instance.productos_db.private_ip}:27017/productos_db?authSource=admin
              NODE_ENV=production
              EOF

              # Instalar dependencias
              sudo npm install

              # Instalar PM2 para gestión de procesos
              sudo npm install -g pm2

              # Iniciar la aplicación con PM2
              sudo pm2 start src/app.js --name productos-service
              sudo pm2 startup systemd
              sudo pm2 save

              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-productos-ms"
    Role = "productos-ms"
  })

  depends_on = [aws_instance.productos_db]
}

# Salida. Muestra la dirección IP privada de la instancia de productos_db (MongoDB).
output "productos_db_private_ip" {
  description = "Private IP address for the Productos Database instance"
  value       = aws_instance.productos_db.private_ip
}

# Salida. Muestra la dirección IP pública de la instancia de productos_db.
output "productos_db_public_ip" {
  description = "Public IP address for the Productos Database instance"
  value       = aws_instance.productos_db.public_ip
}

# Salida. Muestra la dirección IP pública de la instancia de Productos MS.
output "productos_ms_public_ip" {
  description = "Public IP address for the Productos Microservice instance"
  value       = aws_instance.productos_ms.public_ip
}

# Salida. Muestra la dirección IP privada de la instancia de Productos MS.
output "productos_ms_private_ip" {
  description = "Private IP address for the Productos Microservice instance"
  value       = aws_instance.productos_ms.private_ip
}
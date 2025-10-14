# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de Circuit Breaker
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - cbd-traffic-django (puerto 8080)
#    - cbd-traffic-cb (puertos 8000 y 8001)
#    - cbd-traffic-db (puerto 5432)
#    - cbd-traffic-ssh (puerto 22)
#
# 2. Instancias EC2:
#    - cbd-kong
#    - cbd-db (PostgreSQL instalado y configurado)
#    - cbd-monitoring (Monitoring app instalada y migraciones aplicadas)
#    - cbd-alarms-a (Monitoring app instalada)
#    - cbd-alarms-b (Monitoring app instalada)
#    - cbd-alarms-c (Monitoring app instalada)
# ******************************************************************
#!/bin/bash
set -e

echo "[INFO] Start cron service..."

# Crear el archivo de log si no existe
mkdir -p /var/log/cron
touch /var/log/cron/etl.log
chmod 666 /var/log/cron/etl.log

# Iniciar cron en foreground (necesario para que el contenedor se mantenga activo)
cron

echo "[INFO] Cron iniciado. Siguiendo logs..."

# Seguir logs sin crashear si está vacío
tail -f /var/log/cron/etl.log


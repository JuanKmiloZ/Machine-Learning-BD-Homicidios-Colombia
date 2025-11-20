FROM python:3.10-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar cron + cliente MySQL (mariadb-client es el reemplazo)
RUN apt-get update && apt-get install -y --no-install-recommends \
        cron \
        mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /app /var/log/cron

# Copiar scripts del proyecto
COPY ./DL_ETL /app/DL_ETL
COPY ./docker/cron/etl-cron.sh /etc/cron.d/etl-cron.sh
COPY ./docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt /app/requirements.txt

# Permisos cron y entrypoint
RUN chmod 644 /etc/cron.d/etl-cron.sh \
    && chmod +x /entrypoint.sh \
    && crontab /etc/cron.d/etl-cron.sh

# Instalar dependencias Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Definir carpeta de trabajo
WORKDIR /app

# Exponer logs
VOLUME /var/log/cron

# Ejecutar entrypoint
ENTRYPOINT ["/entrypoint.sh"]

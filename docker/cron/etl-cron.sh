# Ejecutar el ETL todos los días a las 02:00 AM
0 2 * * * root /usr/local/bin/python3 /app/DL_ETL/run_all.py >> /var/log/cron/etl.log 2>&1





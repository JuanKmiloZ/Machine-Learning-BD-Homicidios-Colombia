import pandas as pd
import gzip
import logging
from sqlalchemy import text

def load_csv_gzip(conn, df):
    path = "/tmp/homicidios.csv.gz"

    with gzip.open(path, "wt", encoding="utf-8") as f:
        df.to_csv(f, index=False)

    conn.execute(text("SET GLOBAL local_infile=1"))

    sql = f"""
        LOAD DATA LOCAL INFILE '{path}'
        INTO TABLE raw_homicidios
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        IGNORE 1 LINES
        (fecha_hecho, cod_depto, departamento, cod_muni, municipio, zona, sexo, cantidad, fuente);
    """

    conn.execute(text(sql))

import logging
from sqlalchemy import text

def load_partitioned(conn, df):
    for _, row in df.iterrows():
        year = row["fecha_hecho"].year
        month = str(row["fecha_hecho"].month).zfill(2)

        table_name = f"raw_homicidios_{year}_{month}"

        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} LIKE raw_homicidios;
        """))

        insert_sql = f"""
            INSERT INTO {table_name}
            (fecha_hecho, cod_depto, departamento, cod_muni, municipio, zona, sexo, cantidad, fuente)
            VALUES (:fecha_hecho, :cod_depto, :departamento, :cod_muni, :municipio, :zona, :sexo, :cantidad, 'API_HOMICIDIOS')
        """

        conn.execute(text(insert_sql), row.to_dict())

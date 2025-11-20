from sqlalchemy import text
import logging

def load_upsert(conn, df):
    logging.info("Insertando con ON DUPLICATE KEY UPDATE...")

    sql = """
    INSERT INTO raw_homicidios 
    (fecha_hecho, cod_depto, departamento, cod_muni, municipio, zona, sexo, cantidad, fuente)
    VALUES (:fecha_hecho, :cod_depto, :departamento, :cod_muni, :municipio, :zona, :sexo, :cantidad, 'API_HOMICIDIOS')
    ON DUPLICATE KEY UPDATE 
        cantidad = VALUES(cantidad),
        fecha_ingreso = CURRENT_TIMESTAMP;
    """

    conn.execute(text("SET autocommit = 0"))
    for row in df.to_dict(orient="records"):
        conn.execute(text(sql), row)
    conn.execute(text("COMMIT"))

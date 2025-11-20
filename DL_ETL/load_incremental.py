from sqlalchemy import text
import logging

def get_last_date(conn):
    q = text("""
        SELECT last_loaded_date
        FROM etl_control
        WHERE proceso='homicidios_api'
    """)
    r = conn.execute(q).fetchone()
    return r[0] if r else None


def update_last_date(conn, date):
    q = text("""
        INSERT INTO etl_control(proceso, last_loaded_date)
        VALUES('homicidios_api', :d)
        ON DUPLICATE KEY UPDATE last_loaded_date=:d
    """)
    conn.execute(q, {"d": date})


def load_incremental(conn, df):
    last = get_last_date(conn)
    if last:
        logging.info(f"Filtrando > {last}")
        df = df[df["fecha_hecho"] > last]

    if df.empty:
        logging.info("No hay datos nuevos.")
        return

    from DL_ETL.load_upsert import load_upsert
    load_upsert(conn, df)

    max_date = df["fecha_hecho"].max()
    update_last_date(conn, max_date)

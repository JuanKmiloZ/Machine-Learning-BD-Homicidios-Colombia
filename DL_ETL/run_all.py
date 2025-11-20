import logging
from DL_ETL.config import engine
from DL_ETL.extract import fetch_homicidios
from DL_ETL.transform import clean_homicidios
from DL_ETL.load_incremental import load_incremental

def run_all():
    logging.info("=== Iniciando ETL ===")

    df = fetch_homicidios()
    df = clean_homicidios(df)

    with engine.connect() as conn:
        load_incremental(conn, df)

    logging.info("=== ETL Finalizado ===")

if __name__ == "__main__":
    run_all()

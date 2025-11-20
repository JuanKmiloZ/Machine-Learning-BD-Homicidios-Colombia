import pandas as pd
from sodapy import Socrata
import requests as re
import logging

def fetch_api_json(url, limit=50000):
    offset = 0
    all_data = []
    
    while True:
        params = {"$limit": limit, "$offset": offset}
        r = re.get(url, params=params)

        if r.status_code != 200:
            logging.error(f"Error {r.status_code}: {url}")
            break

        data = r.json()
        if not data:
            break

        all_data.extend(data)
        offset += limit

    return pd.DataFrame(all_data)


def fetch_homicidios(limit=350000):
    logging.info("Descargando datos de homicidios desde Socrata...")
    client = Socrata("www.datos.gov.co", None)

    data = client.get("m8fd-ahd9", limit=limit)
    df = pd.DataFrame.from_records(data)

    logging.info(f"Registros descargados: {len(df)}")
    return df


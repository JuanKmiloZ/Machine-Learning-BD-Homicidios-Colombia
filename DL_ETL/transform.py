import pandas as pd
import unicodedata
import logging

def remove_accents(text):
    if not isinstance(text, str):
        return text
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c))

def normalize_text(series):
    return (series.astype(str)
            .str.strip()
            .str.lower()
            .apply(remove_accents)
            .str.title()
    )

def clean_homicidios(df):
    logging.info("Normalizando DataFrame...")

    df["fecha_hecho"] = pd.to_datetime(df["fecha_hecho"], errors="coerce").dt.date
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)

    for col in ["departamento", "municipio", "zona", "sexo"]:
        if col in df:
            df[col] = normalize_text(df[col])

    df = df.dropna(subset=["fecha_hecho"])
    return df


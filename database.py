import sqlite3
import pandas as pd

DB = "db/data.db"


def store_csv(file):

    df = pd.read_csv(file)

    conn = sqlite3.connect(DB)

    df.to_sql("data_table", conn, if_exists="replace", index=False)

    return df


def run_query(query):

    conn = sqlite3.connect(DB)

    result = pd.read_sql_query(query, conn)

    return result
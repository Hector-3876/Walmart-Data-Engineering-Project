import os
import csv
import psycopg2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'walmart-dataset' / 'data'

# Connection details from the Ghost database connection string
DB_HOST = 'fyb69mdaiu.mf6x69efkn.db.ghost.build'
DB_PORT = 5432
DB_NAME = 'tsdb'
DB_USER = 'tsdbadmin'
DB_PASSWORD = 'fnvyu12ayj8vm6q9'

TABLES = [
    ('raw.customers', DATA_DIR / 'customers.csv'),
    ('raw.stores', DATA_DIR / 'stores.csv'),
    ('raw.products', DATA_DIR / 'products.csv'),
    ('raw.employees', DATA_DIR / 'employees.csv'),
    ('raw.orders', DATA_DIR / 'orders.csv'),
    ('raw.order_items', DATA_DIR / 'order_items.csv'),
]


def copy_csv(conn, table_name, csv_path):
    with conn.cursor() as cur:
        with open(csv_path, 'r', encoding='utf-8', newline='') as f:
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
        conn.commit()


if __name__ == '__main__':
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require',
    )
    try:
        for table_name, csv_path in TABLES:
            if not csv_path.exists():
                raise FileNotFoundError(f'Missing file: {csv_path}')
            print(f'Loading {csv_path.name} into {table_name}...')
            copy_csv(conn, table_name, csv_path)
            print(f'Loaded {csv_path.name} into {table_name}')
    finally:
        conn.close()

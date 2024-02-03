import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import psycopg2
from psycopg2 import extras
import datetime
import requests
from typing import List
import logging

from database.data_transformations import transform_row
from database.create_table import create_table
import database.constants_db as cst
from database.count_rows import count_rows


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, force=True)


def get_all_data(last_processed_timestamp: datetime.datetime) -> List[dict]:
    """
    Retrieves all data from the API starting from the last processed timestamp.

    Args:
        last_processed_timestamp (datetime.datetime): The timestamp of the last processed data.

    Returns:
        List[dict]: A list of dictionaries containing the retrieved data.
    """

    n_results = 0
    full_data = []
    while True:
        # The publication date must be greater than the last processed timestamp and the offset (n_results)
        # corresponds to the number of results already processed.
        url = cst.URL_API.format(last_processed_timestamp, n_results)
        response = requests.get(url)
        data = response.json()
        current_results = data["results"]
        full_data.extend(current_results)
        n_results += len(current_results)
        if len(current_results) < cst.MAX_LIMIT:
            break
        # The sum of offset + limit API parameter must be lower than 10000.
        if n_results + cst.MAX_LIMIT >= cst.MAX_OFFSET:
            # If it is the case, change the last_processed_timestamp parameter to the date_de_publication
            # of the last retrieved result, minus one day. In case of duplicates, they will be filtered
            # in the deduplicate_data function. We also reset n_results (or the offset parameter) to 0.
            last_timestamp = current_results[-1]["date_de_publication"]
            timestamp_as_date = datetime.datetime.strptime(last_timestamp, "%Y-%m-%d")
            timestamp_as_date = timestamp_as_date - datetime.timedelta(days=1)
            last_processed_timestamp = timestamp_as_date.strftime("%Y-%m-%d")
            n_results = 0

    logging.info(f"Got {len(full_data)} results from the API")

    return full_data


def deduplicate_data(data: List[dict]) -> List[dict]:
    return list({v["reference_fiche"]: v for v in data}.values())


def query_data() -> List[dict]:
    """
    Queries the data from the API
    """
    full_data = get_all_data(datetime.datetime.min)
    full_data = deduplicate_data(full_data)
    return full_data


def create_postgres_connection():
    """
    Creates a PostgreSQL database connection
    """
    kwargs = {
        arg: getattr(cst, arg) for arg in ["dbname", "user", "password", "host", "port"]
    }
    try:
        connection = psycopg2.connect(**kwargs)
        return connection
    except psycopg2.OperationalError as e:
        logging.error("Database connection failed: %s", e)
        return None


def insert_into_postgres(data, connection):
    """
    Inserts data into PostgreSQL database, ignoring duplicates
    """
    with connection.cursor() as cursor:
        columns = list(data[0].keys())
        query = f"INSERT INTO rappel_conso_table ({', '.join(columns)}) VALUES %s ON CONFLICT (reference_fiche) DO NOTHING"
        data = [tuple([row[col] for col in columns]) for row in data]
        psycopg2.extras.execute_values(
            cursor, query, data, template=None, page_size=100
        )
    connection.commit()


def process_data(row):
    """
    Processes the data from the API
    """
    return transform_row(row)


def stream_to_postgres():
    """
    Writes the API data to PostgreSQL database
    """
    connection = create_postgres_connection()
    if connection:
        logging.info("Creating rappel-conso table ...")
        create_table(connection)
        logging.info("Table creation has finished. Querying data from the API ...")
        results = query_data()
        logging.info("Processing the data ...")
        postgres_data_full = list(map(process_data, results))
        logging.info("Inserting the data in the postgres database ...")
        insert_into_postgres(postgres_data_full, connection)
        logging.info("Checking the number of rows in the rappel-conso table ...")
        n_rows = count_rows(
            database=cst.dbname,
            user=cst.user,
            password=cst.password,
            host=cst.host,
            port=cst.port,
            table="rappel_conso_table",
        )
        logging.info("The number of rows in the rappel-conso table is: %s", n_rows)
        connection.close()


if __name__ == "__main__":
    stream_to_postgres()

import os

from langchain.utilities import SQLDatabase
from .constants_db import port, password, user, host, dbname


url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
table_name = "rappel_conso_table"

db = SQLDatabase.from_uri(
    url,
    include_tables=[table_name],
    sample_rows_in_table_info=1,
)

from typing import Any
import logging

from .constants_db import DB_FIELDS

logger = logging.getLogger(__name__)


def try_execute_sql(connection: Any, sql: str):
    """
    Executes the given SQL statement on the provided database connection.

    Args:
        connection (Any): The database connection object.
        sql (str): The SQL statement to execute.

    Returns:
        None

    Raises:
        Exception: If there is an error executing the SQL statement.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            connection.commit()
            logger.info("Executed table creation successfully")
        except Exception as e:
            logger.info("Couldn't execute table creation due to exception: %s", e)
            connection.rollback()


def create_table(connection):
    """
    Creates the rappel_conso table and its columns.
    """
    create_table_sql = f"""
    CREATE TABLE rappel_conso_table (
        {DB_FIELDS[0]} text PRIMARY KEY,
    """
    for field in DB_FIELDS[1:-1]:
        column_sql = f"{field} text, \n"
        create_table_sql += column_sql

    create_table_sql += f"{DB_FIELDS[-1]} text \n" + ");"
    try_execute_sql(connection, create_table_sql)

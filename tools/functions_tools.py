import ast
import json
from datetime import datetime

from langchain.tools import Tool

from database.sql_db_langchain import db
from tools.tools_constants import COLUMNS_DESCRIPTIONS


def run_query_save_results(db, query):
    """
    Runs a query on the specified database and returns the results.

    Args:
        db: The database object to run the query on.
        query: The query to be executed.

    Returns:
        A list containing the results of the query.
    """
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub]
    return res


def get_categories(query: str) -> str:
    """
    Useful to get categories and sub_categories. A json is returned where the key can be category or sub_category,
    and the value is a list of unique itmes for either both.
    """
    sub_cat = run_query_save_results(
        db, "SELECT DISTINCT sous_categorie_de_produit FROM rappel_conso_table"
    )
    cat = run_query_save_results(
        db, "SELECT DISTINCT categorie_de_produit FROM rappel_conso_table"
    )
    category_str = (
        "List of unique values of the categorie_de_produit column : \n"
        + json.dumps(cat, ensure_ascii=False)
    )
    sub_category_str = (
        "\n List of unique values of the sous_categorie_de_produit column : \n"
        + json.dumps(sub_cat, ensure_ascii=False)
    )

    return category_str + sub_category_str


def get_columns_descriptions(query: str) -> str:
    """
    Useful to get the description of the columns in the rappel_conso_table table.
    """
    return json.dumps(COLUMNS_DESCRIPTIONS)


def get_today_date(query: str) -> str:
    """
    Useful to get the date of today.
    """

    # Getting today's date in string format
    today_date_string = datetime.now().strftime("%Y-%m-%d")
    return today_date_string


def sql_agent_tools():
    tools = [
        Tool.from_function(
            func=get_categories,
            name="get_categories_and_sub_categories",
            description="""
            Useful to get categories and sub_categories. A json is returned where the key can be category or sub_category, 
            and the value is a list of unique items for either both.
            """,
        ),
        Tool.from_function(
            func=get_columns_descriptions,
            name="get_columns_descriptions",
            description="""
            Useful to get the description of the columns in the rappel_conso_table table.
            """,
        ),
        Tool.from_function(
            func=get_today_date,
            name="get_today_date",
            description="""
            Useful to get the date of today.
            """,
        ),
    ]
    return tools

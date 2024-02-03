import psycopg2


def count_rows(database, user, password, host, port, table):
    conn = None
    try:
        conn = psycopg2.connect(
            database=database, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        cur.close()
        return count
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

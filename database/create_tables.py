import psycopg2

from table_queries import (
    users_table,
    submitted_cases_table,
    detected_persons_table,
    default_user_query
)

from postgres import PostgresConnection

def create_tables():
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        table_queries = [
            users_table,
            submitted_cases_table,
            detected_persons_table,
            # default_user_query
        ]
        for query in table_queries:
            try:
                cursor.execute(query)
            except psycopg2.DatabaseError as e:
                print(e)
                pass
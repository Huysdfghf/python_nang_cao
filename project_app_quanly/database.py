import tkinter as tk
import psycopg2
class Database:
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            database=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            if cursor.description:  # Check if the query returns data
                return cursor.fetchall()
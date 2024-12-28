from django.db import connection

def run_sql_query(query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        return results

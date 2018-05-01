import psycopg2

def initialize():
    postgres = psycopg2.connect(host='127.0.0.1', dbname='postgres', user='postgres', password='password')
    def execute(query, values=None):
        cursor = postgres.cursor()
        cursor.execute(query, values)
        postgres.commit()
        data = cursor.fetchall() if cursor.description else []
        cursor.close()
        return data
    return execute

import psycopg2

DB_NAME = "devops_portfolio"
DB_USER = "postgres"
DB_PASS = "devops123"
DB_HOST = "192.168.68.240"
DB_PORT = "5432"

def db_connect():
    conn = 0
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        print("Database connected successfully")
    except:
        print("Database not connected successfully")
db_connect()
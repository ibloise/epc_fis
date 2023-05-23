import getpass
import pymysql
from sqlalchemy import create_engine

def SQL_connect(host = 'localhost', port = 3306, software = "mysql"):
    print(sqlLoader.MSG_CONNECT)
    print(sqlLoader.MSG_USER)
    user = input()
    print(sqlLoader.MSG_PASS)
    password = getpass.getpass()
    try:
        connection = pymysql.connect(host=host,
                    user=user,
                    password=password,
                    port = port
            )
        print(sqlLoader.MSG_SUCCESS)
    except Exception as e:
        print(sqlLoader.MSG_CONNECT_ERROR)
        print(e)
        exit()
    db_data = f'{software.lower()}+pymysql://{user}:{password}@{host}:{port}'
    engine = create_engine(db_data, encoding='latin1')
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    return (db_data, engine, cursor, connection)

def check_schema(schema, cursor):
    cursor.execute("SHOW DATABASES")
    databases = [value for schema in cursor.fetchall() for value in schema.values() ]
    if schema in databases:
        return True
    else:
        return False
    
def get_sql_tables(schema, cursor):
    cursor.execute(f"USE {schema}")
    cursor.execute("SHOW TABLES")
    tables = [value for schema in cursor.fetchall()for value in schema.values()]
    return tables

def create_schema(schema, cursor):
    if not check_schema(schema, cursor):
        cursor.execute(f"CREATE DATABASE {schema}")
        print (f"Se ha creado {schema}")

        
import getpass
import pymysql
from sqlalchemy import create_engine
from constants.constants import sqlLoader

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

    return (db_data, engine, cursor)

def check_schema(schema, cursor):
    cursor.execute("SHOW DATABASES")
    databases = [value for schema in cursor.fetchall() for value in schema.values() ]
    if schema in databases:
        return True
    else:
        return False
    
def build_mysql_tables_query(tables_dict):
    query_dict = {}
    for table, data in tables_dict.items():
        query_dict[table] = f"CREATE TABLE {table} ("
        miniQuery = ""
        for col, structure in data[sqlLoader.COLS_KEY].items():
            if miniQuery:
                miniQuery = ", ".join([miniQuery,f"{col} {structure[sqlLoader.SQL_STRUCTURE_KEY]}" ])
            else:
                miniQuery=f"{col} {structure[sqlLoader.SQL_STRUCTURE_KEY]}"
        query_dict[table] += miniQuery
        if data[sqlLoader.SQL_COMPOSITE]:
            query_dict[table] += f", {data[sqlLoader.SQL_COMPOSITE]}"
        query_dict[table] += ")"
    return query_dict

def get_sql_tables(schema, cursor):
    cursor.execute(f"USE {schema}")
    cursor.execute("SHOW TABLES")
    tables = [value for schema in cursor.fetchall()for value in schema.values()]
    return tables

def get_requirements(tables_dict, requirement_key):
    return {require for table in tables_dict.values() for require in table[requirement_key]}

def check_conflicts (tables_dict, sql_tables ,requirements):
    tables = list(tables_dict.keys())
    if sql_tables:
        print(tables)
        tables += sql_tables
    conflicts = [conflict for conflict in requirements if conflict not in tables]
    if conflicts:
        print("Conflictos en la base de datos. No se puede crear")
        exit()
    else:
        return False

def create_tables(dict_orders, cursor):
    while True:
        if not dict_orders:
            break
        for table in list(dict_orders.keys()):
            query = dict_orders[table]
            try:
                print("Ejecutando:")
                print(query)
                cursor.execute(query)
                del dict_orders[table]
            except Exception as e:
                print("No se ha podido ejecutar:")
                print(query)
                print(e)

def create_schema(schema, cursor):
    if not check_schema(schema, cursor):
        cursor.execute(f"CREATE DATABASE {schema}")
        print (f"Se ha creado {schema}")



def build_database():
    cursor = SQL_connect()[2]
    create_schema(sqlLoader.FIS_SCHEMA, cursor)
    exist_tables = get_sql_tables(sqlLoader.FIS_SCHEMA, cursor)
    create_tables_dict = {key : sqlLoader.TABLES[key] for key in sqlLoader.TABLES if key not in exist_tables}
    if create_tables_dict:
        sql_query_create_orders = build_mysql_tables_query(create_tables_dict)
        requirements = get_requirements(create_tables_dict, sqlLoader.REQUIRE_KEY)
        check_conflicts(create_tables_dict, exist_tables, requirements)
        create_tables(sql_query_create_orders, cursor)
    else:
        print("Nada que crear")

build_database()

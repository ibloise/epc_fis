import utils.sql_utils as sql
from constants.constants import sqlLoader

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


def build_database(cursor):
    sql.create_schema(sqlLoader.FIS_SCHEMA, cursor)
    exist_tables = sql.get_sql_tables(sqlLoader.FIS_SCHEMA, cursor)
    create_tables_dict = {key : sqlLoader.TABLES[key] for key in sqlLoader.TABLES if key not in exist_tables}
    if create_tables_dict:
        sql_query_create_orders = build_mysql_tables_query(create_tables_dict)
        requirements = get_requirements(create_tables_dict, sqlLoader.REQUIRE_KEY)
        check_conflicts(create_tables_dict, exist_tables, requirements)
        create_tables(sql_query_create_orders, cursor)
    else:
        print("Nada que crear")

def main():
    cursor = sql.SQL_connect()[2]
    build_database(cursor)

if __name__ == "__main__":
    main()
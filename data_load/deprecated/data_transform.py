
#Functions that transform and normalize data

# El objetivo de este código es hacer de interfaz con la base de datos para normalizar las cargas
# de cara a posibles cambios en los orígenes de datos.

#Normalización de resultados del CFX:

    # Transformar encabezados
    # Disociar Well, Samples y runs
    # Transformación: calcular delta Ct

#Normalización de microb

    # Transformar encabezados
    # minúsculas a todos
    # Disociar GFHs?? Esto realmente debería hacerlo microb_reader?
    # Traducir tabla de carbas


# v= 0.1 version minima que sirve para capturar los datos. 

#Transformar el sqlLOader.tables para crear las ordenes de pandas

from constants.constants import sqlLoader, cfxData
from cfx_reader import cfx_reader
from microb_reader import microb_reader
from utils.sql_utils import SQL_connect, create_schema


table_name = "patients"
source = "microb"

def get_transform_schema(source, table_name, tables=sqlLoader.TABLES):
    """
    Transforma el diccionario de tablas para crear el renombrador de columnas
    """
    #ToDo: Hay que quitar el hardcode. También hay que poner un par de checks par aver si existe la combinación tabla - source
    table_conf = tables[table_name]
    try:
        src_table = table_conf[sqlLoader.SOURCES_KEY][source]
    except Exception as e:
        print(f'Exception: {e}')
        print(f'{source} not in {table_name}')
        return None
    columns_renamer = {col: confs[source] for col, confs in table_conf[sqlLoader.COLS_KEY].items()}
    renamer = {
    sqlLoader.SRC_SCHEM_KEY: source,
    sqlLoader.SRC_TABLE_KEY: src_table,
    sqlLoader.DEST_TABLE_KEY: table_name,
    sqlLoader.COL_RENAMER_KEY: columns_renamer
    }
    return renamer


def get_source_table_relation():
    """
    Obtiene la relación entre origenes y destinos en el siguiente diccionario:
    origen de datos : {
    tabla origen : tabla destino
    }
    """
    return_dict = {}
    for table, schema in sqlLoader.TABLES.items():
        for key, source in schema[sqlLoader.SOURCES_KEY].items():
            return_dict.setdefault(key, {}).update({source: table})
    return return_dict


def get_col_renamer(source, table_eval):
    table_relation = get_source_table_relation()
    import_keys = table_relation[source]
    try:
        table_des = import_keys[table_eval]
    except Exception as e:
        print(f'Exception: {e}')
        print(f'{table_eval} not in keys')
        return None
    renamer = get_transform_schema(source, table_des)[sqlLoader.COL_RENAMER_KEY] #Lo da al revés...
    renamer = {value: key for key, value in renamer.items()}
    return renamer


def fix_error_key (dict, old_key, new_key):
    if old_key in dict:
        dict[new_key]= dict.pop(old_key)

    else:
        print('No existe la clave')

def normalise_data(reader_dict):
    normalise_data = {}
    for schema, reader in reader_dict.items():
        if reader:
            normalise_data[schema] = {}
            for table_name, df in reader.items():
                print(f'Renombrando {table_name}')
                renamer = get_col_renamer(schema, table_name)
                normalise_data[schema][table_name] = df.rename(columns=renamer)
    return normalise_data



def main():

    data = {}
    try:
        cfx = cfx_reader(store_files=True)
        data[sqlLoader.CFX] = cfx
    except Exception as e:
        print('No se ha podido leer cfx')
        print(e)

    try:
        microb = microb_reader(store_files=True)
        data[sqlLoader.MICROB] = microb
    except Exception as e:
        print('No se ha podido leer microb')
        print(e)

    if not data:
        print('No hay datos')
        exit()
    
    print(data)
    #Apaño
    fix_error_key(data[sqlLoader.CFX], 'Quantification Amplification Results', cfxData.TABLE_CYCLE)

    data = normalise_data(data)

    db_data, engine, cursor, con = SQL_connect()

    orders = {table_name : table for schema in data.values() for table_name, table in schema.items()}
    
    create_schema(sqlLoader.FIS_SCHEMA, cursor)

    for table_name, table in orders.items():
        print(f'cargando {table_name}')
        try:
            table.to_sql(name=table_name, con = engine, schema = sqlLoader.FIS_SCHEMA ,if_exists= 'append', index=False)
            print(f'{table_name} cargada!')
        except Exception as e:
            print(f'No se ha podido cargar {table_name}!')
            print(f'Exception: {e}')


if __name__ == '__main__':
    main()







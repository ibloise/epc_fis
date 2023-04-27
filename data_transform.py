from constants.constants import sqlLoader
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


#Transformar el sqlLOader.tables para crear las ordenes de pandas

from constants.constants import sqlLoader


table = "patients"
schema = "microb"



def get_transform_schema(source, table_name, schema = sqlLoader.TABLES):
    #ToDo: Hay que quitar el hardcode. También hay que poner un par de checks par aver si existe la combinación tabla - source
    table_conf = schema[table_name]
    src_table = table_conf[sqlLoader.SOURCES_KEY][source]
    columns_renamer = {col: confs[source] for col, confs in table_conf["cols"].items()}
    renamer = {
    "src_schema": source,
    "src_table": src_table,
    "dest_table": table_name,
    "column_renamer": columns_renamer
    }
    
    return renamer


print(get_transform_schema(schema,table))

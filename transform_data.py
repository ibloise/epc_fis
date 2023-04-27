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

import pandas as pd
import logging
import argparse
import os
from datetime import datetime
from utils.constants.local_paths import LocalPaths
from utils.constants.load_constants import SqlTables
from utils.sql_tools import SqlConnection
#from data_load.sql_tools import sql_tools



def arg_parser():
    parser = argparse.ArgumentParser(description="Limpieza de duplicados en base de datos FIS")
    parser.add_argument('--test', help = 'Activa el entorno de test',
                        action='store_true')
    parser.add_argument('--verbose', help = 'Set level of verbosity. For debug, set as 10',
                        default=10)
    args = parser.parse_args()
    return args


def set_logger(log_path, loggin_level):
    now = datetime.now().strftime('%Y-%m-%d')
    logger_file = f'{now}_clean_db.log'
    logging.basicConfig(level= loggin_level, filename=os.path.join(log_path, logger_file), 
                    format='%(asctime)s %(levelname)s %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)

    return logger

def main():
    
    local_paths = LocalPaths()

    sql_data = SqlTables()
    local_paths.build_subpaths()
    args = arg_parser()

    logger = set_logger(local_paths.log_paths, args.verbose)

    
    if args.test:
        schema = sql_data.test_schema
    else:
        schema = sql_data.schema
    
    logger.info(f'Selected schema: {schema}')

    

    sql_con = SqlConnection(schema)

    #ToDO: hay que pasar las operaciones de extracción de tablas a SqlConnection o a alguna clase hija

    sql_con.cursor.execute('SHOW TABLES')

    sql_tables = sql_con.cursor.fetchall()

    tables = [table[key] for table in sql_tables for key in table.keys()] #Get SQL tables name

    for table in tables:
        logger.info(f'Reading {table}')
        df = pd.read_sql(f'SELECT * FROM {schema}.{table}', con = sql_con.engine)
        logger.debug(f'{table}: \n {df}')
        df_dedup = df.drop_duplicates()
        logger.debug(f'Dedup {table}: \n {df_dedup}')
        sql_con.launch_table(df_dedup, dest_table=table, action='replace')
        #df_dedup.to_sql(table, con= sql_con.engine, schema=schema, if_exists='replace')
        logging.info(f'{table} cleaned!')

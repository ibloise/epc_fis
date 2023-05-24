

import logging
import os
import sys
from datetime import datetime
from data_load.sql_tools.sql_tools import SqlConnection
from data_load.constants.load_constants import SqlTables
from data_load.constants.local_paths import LocalPaths
from data_load.readers.cfx_reader import group_cfx_files, CfxRun
from data_load.readers.microb_reader import MicrobReader
import argparse
#Set logger


def arg_parser():
    parser = argparse.ArgumentParser(description="Carga de datos a SQL fis")
    parser.add_argument('--test', help = 'Activa el entorno de test',
                        action='store_true')
    parser.add_argument('--verbose', help = 'Set level of verbosity. For debug, set as 10',
                        default=20)
    args = parser.parse_args()
    return args


def set_logger(log_path, loggin_level):
    now = datetime.now().strftime('%Y-%m-%d')
    logger_file = f'{now}.log'
    logging.basicConfig(level= loggin_level, filename=os.path.join(log_path, logger_file), 
                    format='%(asctime)s %(levelname)s %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)

    return logger

def common_config(test):
    sql_tables = SqlTables()
    if test:
        schema = sql_tables.test_schema
    else:
        schema = sql_tables.schema

    sql_connection = SqlConnection(schema)

    local_paths = LocalPaths()
    local_paths.build_subpaths(test)

    return sql_tables, sql_connection, local_paths

def cfx_main():
    args = arg_parser()
    sql_tables, sql_connection, local_paths =  common_config(args.test)
    logger = set_logger(local_paths.log_paths, args.verbose)
    logger.warning('Test mode activate!')
    group_cfx_files(local_paths.cfx_path)
    cfx_runs = [os.path.join(local_paths.cfx_path, folder
                             ) for folder in os.listdir(local_paths.cfx_path) if os.path.isdir(os.path.join(local_paths.cfx_path, folder)) and
                             folder != local_paths.historic]

    for run in cfx_runs:
        logger.info(f'Reading {run}')
        cfx_run = CfxRun(local_paths.cfx_path, run)
        cfx_run.pipeline()
        try:
            sql_connection.launch_table(cfx_run.general_table, sql_tables.pcr_general)

            sql_connection.launch_table(cfx_run.unpivot_melt_data, sql_tables.pcr_melt)

            sql_connection.launch_table(cfx_run.unpivot_ct, sql_tables.pcr_cycle)

            sql_connection.launch_table(cfx_run.run_info, sql_tables.pcr_run_info)

            cfx_run.storage_run(local_paths.cfx_historic)
        except Exception as e:
            logger.error(e)

def microb_main():
    args = arg_parser()
    sql_tables, sql_connection, local_paths =  common_config(args.test)
    logger = set_logger(local_paths.log_paths,args.verbose)
    if args.test:
        logger.warning('Test mode activate!')
    microb_reader = MicrobReader(local_paths.microb_path)

    microb_reader.pipeline()
    try:
        sql_connection.launch_table(microb_reader.patients, sql_tables.sil_patients)

        sql_connection.launch_table(microb_reader.samples, sql_tables.sil_samples)

        sql_connection.launch_table(microb_reader.results, sql_tables.sil_results)

        sql_connection.launch_table(microb_reader.obs, sql_tables.sil_obs)

        microb_reader.storage_files(local_paths.microb_historic)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    microb_main()
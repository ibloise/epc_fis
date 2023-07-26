import pandas as pd
import logging
import argparse
import os
from datetime import datetime
from ..utils.sql_tools import SqlConnection
#from data_load.sql_tools import sql_tools


def arg_parser():
    parser = argparse.ArgumentParser(description="Limpieza de duplicados en base de datos FIS")
    parser.add_argument('--excel', help = 'Excel con el archivo depurado de microb',
                        action='store_true')
    parser.add_argument('--verbose', help = 'Set level of verbosity. For debug, set as 10',
                        default=10)
    args = parser.parse_args()
    return args


def set_logger(log_path, loggin_level):
    now = datetime.now().strftime('%Y-%m-%d')
    logger_file = f'{now}_clean_microb.log'
    logging.basicConfig(level= loggin_level, filename=os.path.join(log_path, logger_file), 
                    format='%(asctime)s %(levelname)s %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)

    return logger


excel_arg = 'dups_microb_data_2023-06-06.xlsx'
excel = pd.read_excel(excel_arg)

sql_connect = SqlConnection('fis_data_temp')

#Download the obs table, update de checker column and load again

# Para la base de datos definitiva IDENTIFICAR CADA ENTRADA DE FORMA ÚNICA


print(excel)
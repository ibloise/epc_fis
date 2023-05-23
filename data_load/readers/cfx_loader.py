import logging
import os
import sys
from datetime import datetime
from data_load.sql_tools.sql_tools import SQL_connection
from cfx_reader import group_cfx_files, CfxRun


root= '/home/microb_ngs/Documents/ivan/test_area/'
log_path = 'logs'
cfx_path = os.path.join(root, 'pcr_epc')

#Set logger

now = datetime.now().strftime('%Y-%m-%d')
logger_file = f'{now}_CFX_READER.log'
logging.basicConfig(level=logging.DEBUG, filename=os.path.join(root, log_path, logger_file), 
                    format='%(asctime)s %(levelname)s %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)

def main():
    group_cfx_files(cfx_path)

    cfx_runs = [os.path.join(cfx_path, folder) for folder in os.listdir(cfx_path) if os.path.isdir(os.path.join(cfx_path, folder))]

    for run in cfx_runs:
        cfx_run = CfxRun(run)

        cfx_run.pipeline()


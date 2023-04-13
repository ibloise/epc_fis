import pandas as pd
import os
import functools
from constants.local_paths import localPaths
from constants.constants import microbData
from utils.utils import return_files

def read_microbdata_batch(files_list, delimiter = microbData.MICROB_DELIM, converters = {microbData.HEAD_NSAMPLE :  str, microbData.HEAD_NHC : str},
                          mo_header = microbData.HEAD_MO):
    reader = functools.partial(pd.read_table, delimiter=delimiter, skiprows=[1,2], encoding="unicode_escape", index_col=False,
                           converters = converters)
    data = [reader(file) for file in files_list]
    data = pd.concat(data)
    data[mo_header] = data[mo_header].str.capitalize()
    data = data[data[microbData.HEAD_DES_RESULT] != microbData.VALUE_PENDING
                ].fillna({microbData.HEAD_MO : microbData.VALUE_NEGATIVE, microbData.HEAD_RESULT : microbData.VALUE_NEGATIVE})
    return  data

def split_dataframes(data, tables_dict):
    return {key : data[value].drop_duplicates() for key, value in tables_dict.items()}


def filter_carba_table(carba_table, result_head = microbData.HEAD_MO, filter_criteria = microbData.VALUE_NEGATIVE):
    return(carba_table[carba_table[result_head] != filter_criteria])

def microb_reader():
    files = return_files(os.path.join(localPaths.DATA_EXCHANGE_PATH, localPaths.MICROB_PATH))
    data = read_microbdata_batch(files)#
    dataframes = split_dataframes(data, microbData.SUBSETS)
    dataframes[microbData.CARBA_TABLE] = filter_carba_table(dataframes[microbData.CARBA_TABLE])
    return dataframes

print(microb_reader())
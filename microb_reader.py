import pandas as pd
import functools
from constants.local_paths import localPaths
from constants.constants import microbData, folderManager
from utils.utils import return_files


#Tables

def read_microbdata_batch(files_list, delimiter = microbData.MICROB_DELIM, usecols = microbData.USE_COLS, converters = {microbData.HEAD_NSAMPLE :  str},
                          mo_header = microbData.HEAD_MO):
    reader = functools.partial(pd.read_table, delimiter=delimiter, skiprows=[1,2], encoding="unicode_escape", index_col=False,
                         usecols=usecols, converters = converters)
    data = [reader(file) for file in files_list]
    data = pd.concat(data)
    data[mo_header] = data[mo_header].str.capitalize()
    return  data

def split_dataframes(data, tables_dict):
    return {key : data[value].drop_duplicates() for key, value in tables_dict.items()}

files = return_files(folderManager.FOLDER_SEP.join([localPaths.DATA_EXCHANGE_PATH, localPaths.MICROB_PATH]))
data = read_microbdata_batch(files).fillna({microbData.HEAD_MO : "Negativo", microbData.HEAD_RESULT : "Negativo"})
dataframes = split_dataframes(data, microbData.SUBSETS)





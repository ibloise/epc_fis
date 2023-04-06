import pandas as pd
import os
import numpy as np
from constants.local_paths import *
from constants.constants import *



def return_files(folder, full_path = True, folder_sep = "/"):
    """
    return list of files paths. If full_path, return absolute paths.
    """
    return [os.path.abspath(folder_sep.join([folder, file])) if full_path else file for file in os.listdir(folder)]

def read_run_info(file, sheet, file_header):
    """
    read run info sheet and return two dataframes: info of run and relation of 
    all excels linked to  run
    """
    try:
        run_info = pd.read_excel(file, sheet_name=sheet, header=None, index_col=0
                ).transpose()
        excel_relation = run_info.iloc[:,[0]].copy()
        excel_relation[file_header] = os.path.basename(file)
        return (run_info.drop_duplicates(), excel_relation)
    except Exception as e:
        print(f"Exception in {file}: {e}")
        return (None, None)

def concat_run_info_path(path, sheet_name, file_header):
    """
    Iterate in path with return files and read all run infos with read_run_info. Concat run_info and excel_relation dataframes
    """
    df_list = [read_run_info(df, sheet=sheet_name, file_header=file_header) for df in return_files(path)]
    run_info, excel_relation = [pd.concat(df_list).drop_duplicates() for df_list in list(zip(*df_list))]
    return (run_info, excel_relation)

def assign_schema_to_file(file, conf_dict, regex_key):
    """
    Cross list of files to read with schemas. Assign schema to each file.
    """
    return_dict = {}
    search_dict = {values[regex_key] :  key for key, values in conf_dict.items()}
    for key, value in search_dict.items():
        if key in file:
            return_dict[file] = conf_dict[value]

    return return_dict

def build_import_orders(conf_dict, data_path, key_reader = KEY_READER, regex_key = KEY_REG_EXP):
    """
    Construct a dictionary of orders based on assign_schema_to_file
    """
    relation = {key : value for file in return_files(data_path) for key, value in assign_schema_to_file(file, conf_dict, regex_key).items()}
    orders = {file : schema for file, schema in relation.items() if schema[key_reader]}
    return orders


def import_cfx_batch_data(orders, key_type = KEY_TYPE, long_format_name = LONG_FORMAT, matrix_format_name = MATRIX_FORMAT,
                        key_datasheet = KEY_DATA_SHEET, key_usecols = KEY_IMPORT_HEADERS,
                        key_run_info_sheet = KEY_RUN_INFO_SHEET, key_regex = KEY_REG_EXP,
                        head_run = HEAD_RUN, head_type = HEAD_TYPE ,engine = "openpyxl"):
    """
    Import excels from CFX runs. Return a tuple with common (non-special) dataframes and reconverted (IN DEVELOP) matrix dataframes
    """
    common_imports = {}
    matrix_imports = {}
    for file,schema in orders.items():
        if schema[key_type] == long_format_name:
            data = pd.read_excel(file, sheet_name=schema[key_datasheet], usecols=schema[key_usecols], engine=engine)
            run = pd.read_excel(file, sheet_name=schema[key_run_info_sheet], header=None, index_col=0, engine=engine).iloc[0,0]
            data[head_run] = run
        #TEMPORAL: ELIMINAR TRAS LA PRIMERA CARGA
            data["Target"] = data["Target"].fillna("Screening")
            if schema[key_regex] not in common_imports.keys():
                common_imports[schema[key_regex]] = [data]
            else:
                common_imports[schema[key_regex]].append(data)
        elif schema[key_type] == matrix_format_name:
            #Desarrollar función específica para transformar las matrices
            pass
    return (common_imports, matrix_imports)

def common_import_transform(common_import_dict, primary_key = [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_RUN], replace_none = True):
    merge_dict = {key : pd.concat(value) for key, value in common_import_dict.items()}
    cross_df = pd.DataFrame()
    for value in merge_dict.values():
        if cross_df.empty:
            cross_df = value
        else:
            cross_df = pd.merge(cross_df, value, on = primary_key)
        if replace_none:
            cross_df = cross_df.replace("None", np.nan).fillna(0)
    return cross_df

def main():
    orders = build_import_orders(cfx_files_features, DATA_EXCHANGE_PATH)
    data = import_cfx_batch_data(orders)
    cross_df = common_import_transform(data[0])
    return cross_df

main().to_excel("test.xlsx")
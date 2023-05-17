import os
import pandas as pd
import numpy as np
from constants.local_paths import localPaths
from constants.constants import cfxData
from utils.utils import return_files, store_file

#Class??


def read_run_info(file, sheet, file_header, store_files):
    """
    read run info sheet and return two dataframes: info of run and relation of 
    all excels linked to  run
    """
    try:
        run_info = pd.read_excel(file, sheet_name=sheet, header=None, index_col=0
                ).transpose()
        excel_relation = run_info.iloc[:,[0]].copy()
        excel_relation[file_header] = os.path.basename(file)
        if store_files:
            store_file(file, store_folder=localPaths.STORE_FOLDER_CFX)
        return (run_info.drop_duplicates(), excel_relation)

    except Exception as e:
        print(f"Exception in {file}: {e}")
        return (None, None)

def concat_run_info_path(path, sheet_name, file_header, store_files):
    """
    Iterate in path with return files and read all run infos with read_run_info. Concat run_info and excel_relation dataframes
    """
    df_list = [read_run_info(df, sheet=sheet_name, file_header=file_header, store_files=store_files) for df in return_files(path) if df != None]
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

def build_import_orders(conf_dict, data_path, key_reader = cfxData.KEY_READER, regex_key = cfxData.KEY_REG_EXP):
    """
    Construct a dictionary of orders based on assign_schema_to_file
    """
    relation = {key : value for file in return_files(data_path) for key, value in assign_schema_to_file(file, conf_dict, regex_key).items()}
    orders = {file : schema for file, schema in relation.items() if schema[key_reader]}
    return orders

def get_run (file, sheet_name, engine):
    return pd.read_excel(file, sheet_name=sheet_name, header=None, index_col=0, engine=engine).iloc[0,0]

def import_tabular(file, sheet_dataset, sheet_run,  head_run, usecols,engine):
    data = pd.read_excel(file, sheet_name=sheet_dataset, usecols=usecols, engine=engine)
    run = get_run(file, sheet_run, engine)
    data[head_run] = run
    #TEMPORAL: ELIMINAR TRAS LA PRIMERA CARGA
    print("Ojo!!!!! Sigue el código temporal en cfx_reader.import_tabular")
    data["Target"] = data["Target"].fillna("Screening")
    return data

def import_matrix(file, sheet_dataset, sheet_run,  head_run,index_col,engine, value_name = cfxData.VALUE, var_name = cfxData.HEAD_WELL, fix_well = True):

    run = get_run(file, sheet_name=sheet_run,engine=engine)
    matrix = pd.read_excel(file, sheet_name=sheet_dataset, usecols=lambda x: "Unnamed" not in x).melt(id_vars=index_col, 
                            var_name = var_name, value_name = value_name)
    matrix[head_run] = run
    if fix_well:
        # well format is A01 in long dataframes and A1 in wide dataframes. This code fix them
        matrix[var_name] = matrix[var_name].apply(lambda x :  x if (len(x) > 2) else (x[0] + "0" + x[1])) 
    return matrix

def append_list_dict(dictionary, element_to_append, key):
    print(key)
    if key not in dictionary.keys():
        dictionary[key] = [element_to_append]
    else:
        dictionary[key].append(element_to_append)
    return dictionary

def import_cfx_batch_data(orders, store_files = True,key_type = cfxData.KEY_TYPE, long_format_name = cfxData.LONG_FORMAT, 
                        matrix_format_name = cfxData.MATRIX_FORMAT,
                        key_datasheet = cfxData.KEY_DATA_SHEET, key_usecols = cfxData.KEY_IMPORT_HEADERS,
                        key_run_info_sheet = cfxData.KEY_RUN_INFO_SHEET, key_regex = cfxData.KEY_REG_EXP,
                        head_run = cfxData.HEAD_RUN, key_id_head = cfxData.KEY_ID_HEADER, head_well = cfxData.HEAD_WELL,
                        head_sample = cfxData.HEAD_SAMPLE,
                        key_value = cfxData.KEY_PIVOT_VALUE_HEADER,
                        engine = "openpyxl"):
    """
    Import excels from CFX runs. Return a tuple with common (non-special) dataframes and reconverted (IN DEVELOP) matrix dataframes
    """
    common_imports = {}
    matrix_imports = {}
    matrix_imports_fix = {}
    well_samples = pd.DataFrame(columns=[head_run, head_well, head_sample])

    for file,schema in orders.items():
        parameters = (schema[key_datasheet], schema[key_run_info_sheet], head_run)
        if schema[key_type] == long_format_name:
            data = import_tabular(file, *parameters,
                                      usecols=schema[key_usecols], engine=engine)
            well_samples = pd.concat([well_samples, data[[head_run, head_well, head_sample]]]).drop_duplicates(ignore_index=True)
            common_imports = append_list_dict(common_imports, data, schema[key_regex])

        elif schema[key_type] == matrix_format_name:
            data = import_matrix(file, *parameters, index_col=schema[key_id_head], value_name = schema[key_value], engine=engine)
            matrix_imports = append_list_dict(matrix_imports, data, schema[key_regex])
        if store_files: #Habría que hacer un único punto de store files
            store_file(file, store_folder=localPaths.STORE_FOLDER_CFX)
        #cross data
        
        for key, value in matrix_imports.items():
            new_values = [pd.merge(data, well_samples, on = [head_run, head_well], how="left") for data in value] #Este codigo reconstruye las muestras a partir de las wells
            matrix_imports_fix[key] = new_values

    return (common_imports, matrix_imports_fix)


def common_import_transform(common_import_dict,common_table_name, primary_key = [cfxData.HEAD_WELL, cfxData.HEAD_FLUOR, cfxData.HEAD_TARGET, cfxData.HEAD_SAMPLE, cfxData.HEAD_RUN], 
                            replace_none = True):
    merge_dict = {key : pd.concat(value) for key, value in common_import_dict.items()} #Merge dataframe by key
    cross_df = pd.DataFrame()
    for value in merge_dict.values(): 
        if cross_df.empty:
            cross_df = value #Create first dataframe
        else:
            cross_df = pd.merge(cross_df, value, on = primary_key) #Join all data
        if replace_none:
            cross_df = cross_df.replace("None", np.nan).fillna(0) #Replace NA and None by 0s (cycle and temperature data are NAs in CFX)
    return {common_table_name: cross_df}

def matrix_import_transform(matrix_import_dict):
    """
    Concat matrix dataframe
    """
    return {key:pd.concat(values, ignore_index=True) for key, values in matrix_import_dict.items()}

def concat_dict_dataframes (dataframes_dict, keys_to_concat, primary_key, novel_key):
    """
    Concat dictionary of dataframes based on keys_to_concat list with primary_key
    """
    new_dict = {novel_key: pd.DataFrame()}
    for key, data in dataframes_dict.items():
        if key in keys_to_concat:
            if new_dict[novel_key].empty:
                new_dict[novel_key] = data
            else:
                new_dict[novel_key] = new_dict[novel_key].merge(data, on = primary_key, how="outer")
        else:
            new_dict[key] = data
    return new_dict

def cfx_reader(store_files = False):
    path = os.path.join(localPaths.DATA_EXCHANGE_PATH, localPaths.CFX_PATH)
    run_info, excel_relation = concat_run_info_path(path, sheet_name=cfxData.RUN_INFO, file_header=cfxData.HEAD_EXCEL_FILE, store_files=store_files)
    return_dfs = {cfxData.TABLE_RUN_INFO : run_info, cfxData.TABLE_EXCELS : excel_relation}
    
    orders = build_import_orders(cfxData.cfx_files_features, path)
    data = import_cfx_batch_data(orders, store_files=store_files)

    #transform the common import table
    cross_df = common_import_transform(data[0], common_table_name=cfxData.TABLE_GENERAL)
    return_dfs.update(cross_df)
    
    #Transform matrix data

    matrix_dict = matrix_import_transform(data[1])
    matrix_dict = concat_dict_dataframes(matrix_dict, [cfxData.MELT_CURVE_DERIVATE, cfxData.MELT_CURVE_RFU],
                                         primary_key = [cfxData.HEAD_WELL, cfxData.HEAD_TEMPERATURE,
                                               cfxData.HEAD_RUN, cfxData.HEAD_SAMPLE],
                                               novel_key=cfxData.TABLE_MELT)
    print(matrix_dict.keys())
    return_dfs.update(matrix_dict)
    return_dfs = {key : df.drop_duplicates() for key, df in return_dfs.items()}
    return return_dfs


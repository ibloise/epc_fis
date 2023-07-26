import pandas as pd
from datetime import datetime
from ..utils.sql_tools import SqlConnection
from .readers.renamers import SIL_renamer
from ..utils.constants.load_constants import SqlTables


def main():

    print('Warning: This script run without logger')
    now = datetime.now().strftime('%Y-%m-%d')
    sql_connect = SqlConnection('fis_data_temp')
    sil_metadata = SIL_renamer()
    sql_tables = SqlTables()
    obs = pd.read_sql('SELECT * FROM obs', sql_connect.engine)
    print('Get obs table')

    duplicated = obs.duplicated(subset=['sample_name', 'obs'], keep=False)

    dup_df = obs[duplicated].sort_values(['sample_name', 'obs'])
    print('Table deduplicated')
    cods = list(dup_df[sil_metadata.cod_mo].drop_duplicates())

    cods_sentence = ','.join(f'"{value}"' for value in cods)

    cods_microorg = pd.read_sql(f'SELECT {sil_metadata.cod_mo},  {sil_metadata.des_mo} from {sql_tables.sil_results} WHERE {sil_metadata.cod_mo} in ({cods_sentence})',
                                sql_connect.engine).drop_duplicates()

    dup_df = dup_df.merge(cods_microorg, how='left', on=sil_metadata.cod_mo)

    dup_df.to_excel(f'dups_microb_data_{now}.xlsx', index=False)
    print('Excel writed!')
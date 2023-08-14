from ..utils.constants.load_constants import SqlTables
from ..analysis.samples import StudySample
from ..utils.sql_tools import SqlConnection


def common_config(test):
    sql_tables = SqlTables()
    if test:
        schema = sql_tables.test_schema
    else:
        schema = sql_tables.schema

    sql_connection = SqlConnection(schema)

    return sql_tables, sql_connection


def create_working_order(check_table, sql_conn, sql_tables):
    query = sql_conn.create_table_query(sql_tables.pcr_general, [sql_tables.sample])
    samples_in_project = sql_conn.execute_table_query(query).drop_duplicates()[sql_tables.sample].to_list()

    if sql_conn.check_exist_table(check_table):
    #Descargamos todas las muestras vs todas las que estan en generate meltin
        query = sql_conn.create_table_query(check_table, [sql_tables.sample])
        exist_samples = sql_conn.execute_table_query(query).drop_duplicates()[sql_tables.sample].to_list()

        working_samples = [sample for sample in samples_in_project if sample not in exist_samples]
    else:
        working_samples = samples_in_project

    return working_samples


def set_sample(sample, sql_conn):
        study_sample = StudySample(sample)
        study_sample.connect_db(sql_conn)

        study_sample.get_screening()

        study_sample.get_spec()

        study_sample.get_melting()

        study_sample.calc_all_melt_temps()
        study_sample.calc_delta_ct()

        return study_sample

def load_df(df, destiny_table, id_col, id_value, sql_conn):
    if not df.empty:
        df[id_col] = id_value
        sql_conn.launch_table(df, destiny_table)

def main():
    #melting
    sql_tables, sql_conn = common_config(False)
    melt_working_list = create_working_order(sql_tables.generate_melting, sql_conn, sql_tables)
    cq_working_list = create_working_order(sql_tables.generate_delta, sql_conn, sql_tables)

    both_list = set(melt_working_list).intersection(cq_working_list)

    only_melt = [sample for sample in melt_working_list if sample not in both_list]

    only_cq = [sample for sample in cq_working_list if sample not in both_list]
    
    for sample in both_list:
        print(f'Loading {sample}')

        study_sample = set_sample(sample, sql_conn)

        load_df(study_sample.melt_temps_df,
                sql_tables.generate_melting,
                id_col = sql_tables.sample,
                id_value = study_sample.sample_id,
                sql_conn = sql_conn)
        
        load_df(study_sample.delta_cq_df,
                sql_tables.generate_delta,
                id_col = sql_tables.sample,
                id_value = study_sample.sample_id,
                sql_conn = sql_conn)
    
    for sample in only_melt:
        print('Loading only melts')
        print(f'Loading {sample}')

        study_sample = set_sample(sample, sql_conn)

        load_df(study_sample.melt_temps_df,
                sql_tables.generate_melting,
                id_col = sql_tables.sample,
                id_value = study_sample.sample_id,
                sql_conn = sql_conn)

    for sample in only_cq:
        print('Loading only cqs')
        print(f'Loading {sample}')

        study_sample = set_sample(sample, sql_conn)

        load_df(study_sample.delta_cq_df,
                sql_tables.generate_delta,
                id_col = sql_tables.sample,
                id_value = study_sample.sample_id,
                sql_conn = sql_conn)
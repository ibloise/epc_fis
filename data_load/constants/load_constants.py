from dataclasses import dataclass


@dataclass

class SqlTables():

    test_schema: str = 'fis_data_test'
    schema: str = 'fis_data_temp'

    #PCR tables
    pcr_run_info: str = 'run_info'
    pcr_general: str = 'pcr_data'
    pcr_melt: str = 'melting_data'
    pcr_cycle: str = 'cycle_data'


    #sil_tables

    sil_patients: str = 'patients'
    sil_samples: str = 'samples'
    sil_results: str= 'results'
    sil_obs: str = 'obs' 


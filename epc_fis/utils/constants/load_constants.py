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

    #pcr_tables

    #Headers
    sample: str='sample'
    sample_name: str='sample_name'
    cod_mo: str='cod_microorganism'
    obs: str = 'obs'
    cq: str = 'cq'
    target: str='target'
    run: str='run'
    well: str ='well'
    melt_derivate: str='melt_derivative_value'
    temperature: str='temperature'
    melt_rfu: str='melt_rfu_value'

    #Generate tables

    generate_melting: str="calc_melting"
    generate_delta: str="delta_cq"
    #key values

    val_screening = 'Screening'


import pandas as pd
from ..utils.sql_tools import SqlConnection

#Limpiar hardcoding!!!!
sql_connect = SqlConnection('fis_data_temp')

pcr = pd.read_sql('SELECT * FROM pcr_data', sql_connect.engine)

samples = pd.read_sql('SELECT * from results', sql_connect.engine)

obs = pd.read_sql('SELECT * from obs', sql_connect.engine)

pcr = pcr[pcr.columns.drop(list(pcr.filter(regex='origin_file')))]

pcr['cq'] = pcr['cq'].fillna(0)

#pcr['result'] = np.where(pcr['cq'] > 0, 'positivo', 'negativo')


checker = pcr[['sample', 'run', 'target', 'cq']]

check_screen = checker.query('target == "Screening"')
check_not_screen = checker.query('target != "Screening"')


data_16S = check_not_screen.query('target == "16S"')[['sample', 'run', 'cq']]
data_for_work = check_not_screen.query('target != "16S"').merge(data_16S, on=['sample', 'run'], how='left', suffixes=['_value', '_16S'])

data_for_work['delta_cq'] = data_for_work['cq_value'] - data_for_work['cq_16S']

data_for_work.to_excel('data_for_work.xlsx')

check_not_screen.to_excel('check_with_Screen.xlsx')

check_screen.to_excel('screening.xlsx')
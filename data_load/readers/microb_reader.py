from readers.renamers import SIL_renamer
import pandas as pd
import numpy as np
import os
import logging
import shutil
import sys

logger = logging.getLogger(__name__)

class MicrobReader(SIL_renamer):
    def __init__(self, path):

        logger.info('Creating new MicrobReader class')

        self.path = path

        logger.info(f'Reading path: {self.path}')

        check_dir = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]
        if not check_dir:
            logging.info('No files to read')
            sys.exit()
        #attributes
        self._delim = '|'
        #headers
            #patients
        self._head_nhc = 'nºhistoria'
        self._head_afi = 'afi'
        self._head_surna_1 = 'Apellido1'
        self._head_surna_2 = 'Apellido2'
        self._head_name = 'Nombre'
        self._head_sex = 'Sexo'
        self._head_birthd = 'Fec.Nacimiento'

        self._cols_patients = [
            self._head_nhc,
            self._head_afi,
            self._head_surna_1,
            self._head_surna_2,
            self._head_birthd,
            self._head_sex,
        ]

             # Samples
        self._head_sample_name = 'NºMuestra'
        self._head_entry_date = 'Fec.Entrada'
        self._head_cod_origin = 'Cod.Procedencia'
        self._head_des_origin = 'Des.Procedencia'
        self._head_cod_serv = 'Cod.Servicio'
        self._head_des_serv = 'Des.Servicio'
        self._head_room = 'Habitacion'
        self._head_cod_muestra = 'Cod.Muestra'
        self._head_des_muestra = 'Des.Muestra'
        self._head_cod_analisis = 'Cod.Analisis'
        self._head_des_analisis = 'Des.Analisis'
        self._head_result_date = 'Fec.Resultado'

        self._cols_samples = [
            self._head_sample_name,
            self._head_entry_date,
            self._head_cod_origin,
            self._head_des_origin,
            self._head_cod_serv,
            self._head_des_serv,
            self._head_room,
            self._head_cod_muestra,
            self._head_des_muestra,
            self._head_cod_analisis,
            self._head_des_analisis,
            self._head_result_date

        ]

        self._head_result = 'Des.Resultado'
        self._head_cod_mo = 'Cod.Microorganismo'
        self._head_mo = 'Des.Microorganismo'

        self._cols_results = [
            self._head_sample_name,
            self._head_result,
            self._head_cod_mo,
            self._head_mo
        ]

        self._head_cod_obs = 'Cod.Observaciones.1'

        self._cols_obs = [
            self._head_sample_name,
            self._head_cod_mo,
            self._head_cod_obs
        ]

        #rename headers:

            #gfhs

        self._head_des_gfh = 'des_GFH'
        self._head_cod_gfh = 'cod_GFH'

            #values
        self._value_pend = 'PENDIENTE DE RESULTADO'
        self._value_cod_neg = 'neg'
        self._value_no_obs = 'no_obs'
        self._value_cpc = 'CPC' #Considerar precauciones de contacto
        self._value_atb = 'ATB' #Muestra pendiente de antibiograma

        self._list_del_obs= [
            self._value_cpc,
            self._value_atb
        ]
        #Concat files
        self.data = self.concat_files()

        #init list in father class

        self.create_lists()

    def read_microb_file(self, file):
        logger.info(f'Reading file: {file}')
        data = pd.read_table(file, delimiter=self._delim,
                             skiprows=[1,2], encoding="unicode_escape",
                             converters={
                                 self._head_sample_name : str,
                                 self._head_nhc: str
                             },
                             index_col=False
                             )
        return data

    def yield_files(self):
        for file in os.listdir(self.path):
            full_path = os.path.join(self.path, file)
            if os.path.isfile(full_path):
                yield full_path

    def concat_files(self):
        data = pd.concat([self.read_microb_file(file) for file in self.yield_files()])
        return data
    
    def _build_gfh_table(self):
        cods = pd.concat([self.gfhs[self._head_cod_origin], self.gfhs[self._head_cod_serv]], ignore_index=True).drop_duplicates()
        logger.debug(f'GFH cods table: \n {cods.to_string()}')
        des = pd.concat([self.gfhs[self._head_des_origin], self.gfhs[self._head_des_serv]], ignore_index=True).drop_duplicates()
        logger.debug(f'GFH description table: \n {des.to_string()}')

        self.gfhs = pd.DataFrame({self._head_cod_gfh: cods, self._head_des_gfh: des}).drop_duplicates()
        logger.debug(f'GFHs table: \n {self.gfhs.to_string()}')
    
    def _clean_results(self):
        #Drop pending
        logger.info('Drop pending values')
        self.results = self.results.drop(self.results[self.results[self._head_result] == self._value_pend].index)
        # Join negatives with mo
        logger.info('Joining fields')
        self.results[self._head_mo] = np.where(
            self.results[self._head_mo].isna(),
            self.results[self._head_result],
            self.results[self._head_mo])
        
        # Drop all results columns
        self.results = self.results.drop(self._head_result, axis=1)

        # Linnean nomenclature:
        logger.info('Change microorganismo to linnean nomenclature')
        self.results[self._head_mo] = self.results[self._head_mo].str.capitalize()

        #Cod negative == neg
        self.results[self._head_cod_mo] = self.results[self._head_cod_mo].fillna(self._value_cod_neg)
        #Todo: realmente en results solo debería estar el código del mo. Tras el cambio de SIL habría que intentar mapear por SNOMED y dejar una única tabla

        self.results = self.results.drop_duplicates()
        logger.debug(f'Results table cleaned: \n {self.results.to_string()}')

    def _clean_obs(self):
        logger.info('Clean obs')
        self.obs = self.obs.dropna(subset=self._head_cod_mo)
        self.obs[self._head_cod_obs] = self.obs[self._head_cod_obs].fillna(self._value_no_obs)

        mask = self.obs[self._head_cod_obs].isin(self._list_del_obs)

        self.obs = self.obs[~mask] # ~ invert the mask
        logger.debug(f'Obs cleaned: \n {self.obs.to_string()}')

    def split_data(self):
        '''
        Split the data obtained from Microb into different SQL-like datasets.
        '''

        logger.info('Splitting data')
        self.patients = self.data[self._cols_patients].drop_duplicates()

        self.samples = self.data[self._cols_samples].drop_duplicates()

        self.gfhs = self.data[[self._head_cod_origin, self._head_des_origin,self._head_cod_serv, self._head_des_serv]].drop_duplicates()

        self._build_gfh_table()
        
        self.results = self.data[self._cols_results].drop_duplicates() 

        self._clean_results()

        self.obs = self.data[self._cols_obs].drop_duplicates()

        self._clean_obs()

        logger.info('Data splitted!')

    def renamer_table(self, table, new_cols, old_cols):

        renamer_dict = self.create_dict_renamer(new_cols, old_cols)
        if not renamer_dict:
            logger.error('Cannot create renamer dict!!')
            return None
        logger.debug(f'Renamer dict: {renamer_dict}')
        return_table = table.rename(columns = renamer_dict)

        return return_table

    def renamer_data(self):
        logger.info('Renaming tables')
        #Renaming table patients

        self.patients = self.renamer_table(self.patients, self.cols_patients,self._cols_patients)

        self.samples = self.renamer_table(self.samples, self.cols_samples, self._cols_samples)

        self.results = self.renamer_table(self.results, self.cols_results, self._cols_results)

        self.obs = self.renamer_table(self.obs, self.cols_obs, self._cols_obs)

    def pipeline(self):
        logger.info('Running MicrobReader pipeline')
        self.split_data()
        self.renamer_data()
        logger.info('Pipeline finished!')

    def storage_files(self, storage_folder):
        storage_folder = os.path.join(self.path, storage_folder)
        for file in self.yield_files():
            try:
                shutil.move(file, storage_folder)
                logging.info(f'File {file} moved!')
            except Exception as e:
                logging.error(f'Cannot move {file}')
                logging.error(e)
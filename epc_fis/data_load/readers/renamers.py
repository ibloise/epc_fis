from dataclasses import dataclass
import logging
# Remember: dataclasses requires python >3.7
# list use in dataclasses requires python >= 3.9


logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class SIL_renamer:

    #patients
    nhc: str = 'nhc'
    afi: str = 'afi'
    name: str = 'name'
    last_name_1: str = 'last_name_1'
    last_name_2: str = 'last_name_2'
    sex: str = 'sex'
    birth_date: str = 'birth_date'

    #samples
    sample_name: str = 'sample_name'
    entry_date: str = 'entry_date'
    cod_origin: str = 'cod_origin'
    des_origin: str = 'des_origin'
    cod_serv: str = 'cod_serv'
    des_serv: str = 'des_serv'
    cod_room: str = 'cod_room'
    cod_sample: str = 'cod_sample'
    des_sample: str = 'des_sample'
    cod_analisis: str = 'cod_analisis'
    des_analisis: str = 'des_analisis'
    result_date: str = 'result_date'


    
    #result
    result: str = 'result'
    cod_mo: str = 'cod_microorganism'
    des_mo: str = 'des_microorganism'

    #observ

    cod_obs: str = 'obs'



    def create_lists(self): #This method must be called in init method of daughter class
        self.cols_patients =  [self.nhc, self.afi, self.name, self.last_name_1, self.last_name_2, self.sex, self.birth_date]

        self.cols_samples = [self.sample_name, self.entry_date, self.cod_origin, self.des_origin, 
                       self.cod_serv,self.des_serv ,self.cod_room, self.cod_sample, self.des_sample,
                       self.cod_analisis, self.des_analisis, self.result_date]
        
        self.cols_results = [self.sample_name, self.result, self.cod_mo, self.des_mo]

        self.cols_obs = [self.sample_name, self.cod_mo, self.cod_obs]

    def create_dict_renamer(self, new_cols, origin_cols): #Remember: pandas require {old_col :  new_col}
        if len(new_cols) != len(origin_cols):
            logger.error(f'Both list must be have the same length')
            logger.debug(f'old list({len(origin_cols)}): {origin_cols}')
            logger.debug(f'new list({len(new_cols)}): {new_cols} ')
            return None
        
        return {old_element: new_element for old_element, new_element in zip(origin_cols, new_cols)}
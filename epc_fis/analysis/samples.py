import pandas as pd
import sys
import numpy as np
from scipy.signal import  find_peaks
from itertools import product
import matplotlib.pyplot as plt
from ..utils.constants.load_constants import SqlTables

class StudySample():
    #Esta clase se pasa el SOLID por el arco, Hay que refactorizarla en algun momento
    SQL_TABLES = SqlTables()

    MIN_MELT_TEMP = 75

    KEY_MELT_TEMP = 'melt_temp'
    KEY_MELT_RFU = 'melt_rfu'
    KEY_THRESHOLD = 'threshold'

    KEY_16S = "16S"
    KEY_DELTA_CQ = "delta_cq"
    KEY_LOG_DELTA_CQ = "log_delta_cq"
    KEY_CQ_16S = "cq_16S"
    KEY_CQ_TARGET = "cq_target"
    KEY_CQ_16S_CP = "cq_16s_control"
    KEY_CQ_TARGET_CP = "cq_target_control"

    def __init__(self, sample_id):
        self.sample_id  = sample_id
    
    def connect_db(self, sql_connection):
        """
        Store connection object for query database
        """
        self.connection = sql_connection
    
    def get_screening(self):
        """
        get screening data from database
        """
        query = f"""
        SELECT * FROM {self.SQL_TABLES.pcr_general} 
        WHERE {self.SQL_TABLES.target} = '{self.SQL_TABLES.val_screening}' AND {self.SQL_TABLES.sample} = '{self.sample_id}'
        """
        self.screening_pcr = self._execute_query(query)

        if len(self.screening_pcr) > 1:
            print("WARNING: More than two records have been detected in the query. Please review the data.")

    def get_spec(self):
        """
        Get specific PCRs
        """

        query = self._create_query(self.SQL_TABLES.pcr_general, headers="*", sample_header=self.SQL_TABLES.sample)

        #refine query:

        query = query + f" AND {self.SQL_TABLES.target} != '{self.SQL_TABLES.val_screening}'"

        self.spec_pcr = self._execute_query(query)

        if self.spec_pcr.empty:
            print('INFO: No specific PCR data found')
            return None

        #Importante, antes de esto habría que hacer la transformación del 16S. Siempre van a existir duplicados

        if self.spec_pcr.duplicated(subset=[self.SQL_TABLES.sample, self.SQL_TABLES.target]).any():
            print("WARNING: There are duplicate values for some elements. Please review the data.")

    def check_array(self, np_array):
        try:
            np_array = np.array(np_array)
            return True
        except Exception as e:
            print("Object derivate_rfu must be a numpy array or convertible to one.")
            print("Error:")
            print(e)
        return False
    
    def _execute_query(self, query):
        if not hasattr(self, 'connection'):
            sys.exit("""
            Error in _execute_query: This method require connection to database. Execute StudySample.connect_db and try again
            """)
        
        df = pd.read_sql(query, self.connection.engine)
        
        return df
    
    def manage_duplicates(self): #Method to deal with duplicated data
        pass
    
    def get_melting(self): #Method to get melting data from databases
        """
        get melting data
        """
        headers = [
            self.SQL_TABLES.temperature,
            self.SQL_TABLES.well,
            self.SQL_TABLES.sample,
            self.SQL_TABLES.melt_rfu,
            self.SQL_TABLES.melt_derivate,
            self.SQL_TABLES.run
        ]

        query = self._create_query(self.SQL_TABLES.pcr_melt, headers, self.SQL_TABLES.sample)

        self.melting_distribution = self._execute_query(query)
        
        #recover well info

        cross_key = [
            self.SQL_TABLES.well,
            self.SQL_TABLES.sample,
            self.SQL_TABLES.run
        ]
        headers = cross_key + [self.SQL_TABLES.target]

        query = self._create_query(self.SQL_TABLES.pcr_general, headers, self.SQL_TABLES.sample)

        well_info = self._execute_query(query).drop_duplicates(headers)

        self.melting_distribution = self.melting_distribution.merge(well_info, how='left',
                                                            on = cross_key)

    def _create_query(self, table, headers, sample_header, sample_id = None):
        if headers == '*':
            select_statement = '*'
        else:
            select_statement = ", ".join(headers)

        if not sample_id:
            sample_id = self.sample_id

        query = f"""
        SELECT {select_statement} FROM {table}
        WHERE {sample_header} = '{sample_id}'
        """

        return query
    
    def calc_melting_peaks(self, derivate_rfu, mode = "multimodal"):
        """
    Calculate the indices of melting peaks in a RFU derivative melting curve data.

    Usage:
        calc_melting_peaks(derivate_rfu, mode="multimodal")

    Args:
        derivate_rfu (array-like or np.ndarray): Numpy array or any object that can be coerced to an array, representing the distribution of melting RFU derivative data.
        mode (str): Mode to find peaks. Options: "multimodal" (return all peaks above threshold), "unimodal" (return only the max peak).

    Returns:
        filtered_peaks (list): List of indices corresponding to the peaks.
        """

        if not self.check_array(derivate_rfu):
            return None
 
        if mode == "multimodal":
            peaks, _ = find_peaks(derivate_rfu, distance=1)
        elif mode == "unimodal":
            peaks = [int(np.argmax(derivate_rfu))]
        else:
            print("ERROR: mode argument only accepts unimodal or multimodal")
            return None

        return peaks

    def calc_all_melt_temps(self):
        
        #Todas las combinaciones de target y run:
        data_list = []
        #combinations = list(product(self.melting_distribution[self.SQL_TABLES.run].unique(),
        #                            self.melting_distribution[self.SQL_TABLES.target].unique()))
        
        combs = self.melting_distribution[[self.SQL_TABLES.run, self.SQL_TABLES.target]].drop_duplicates()


        combinations = [tuple(row[name] for name in [self.SQL_TABLES.run, self.SQL_TABLES.target]) for _, row in combs.iterrows()]
        for comb in combinations:

            #Salimos del 16S:
            if comb[1] == self.KEY_16S:
                continue

            subset = self.melting_distribution.query(
                f"{self.SQL_TABLES.run} == '{comb[0]}' & {self.SQL_TABLES.target} == '{comb[1]}'")
            
            melt_temps, melt_rfus, threshold = self.calc_melt_temp(subset)
            
            if melt_temps.size == 0:
                melt_temps = [0]
                melt_rfus = [0]

            for idx, temp in enumerate(melt_temps):
                data_dict = {
                    self.KEY_MELT_TEMP : temp,
                    self.KEY_MELT_RFU : melt_rfus[idx],
                    self.KEY_THRESHOLD  : threshold,
                    self.SQL_TABLES.run : comb[0],
                    self.SQL_TABLES.target : comb[1]
                }

                data_list.append(data_dict)
        
        self.melt_temps_df = pd.DataFrame(data_list)

    def calc_melt_temp(self,df): #Calculate melting temperature of isolate
        #Select melting_range
        df = df.query(f"{self.SQL_TABLES.temperature} > {self.MIN_MELT_TEMP}")
        derivate = np.array(df[self.SQL_TABLES.melt_derivate])
        temperature = np.array(df[self.SQL_TABLES.temperature])
        #locals_max_idx = argrelmin(derivate)
        #locals_max = derivate[locals_max_idx[0]]

        peaks = self.calc_melting_peaks(derivate)

        filtered_peaks, threshold = self.filter_melting_peaks(derivate, peaks)

        melt_rfu = derivate[filtered_peaks]

        melt_temp = temperature[filtered_peaks]

        return melt_temp, melt_rfu, threshold

    def filter_melting_peaks(self, derivate_rfu, peaks, threshold_coeff = 1.7):

        if not self.check_array(derivate_rfu):
            return None
        else:
            derivate_rfu = np.array(derivate_rfu)
        threshold = threshold_coeff * derivate_rfu.mean()

        filtered_peaks = [peak for peak in peaks if derivate_rfu[peak] > threshold]

        return filtered_peaks, threshold

    def plot_melt_curve(self, temperature, derivate, filtered_peaks, threshold, label = ''):
        plt.plot(temperature, derivate, label = label)
        plt.plot(temperature[filtered_peaks], derivate[filtered_peaks], 'ro')
        plt.axhline(threshold,linestyle = "--", color = "red")
        plt.legend()
        plt.show()

    def calc_delta_ct(self): #Record delta ct of specific targets
        #Lógica: partimos de self.spec_pcr. QUitamos todas las columnas que molestan
        # Iteramos osbre los runs. Para cada RUn
        #   Consultamos el CP de ese Run a la base de datos
        #   Almacenamos el 16S problema y el 16S del CP
        #   Para cada posible nivel de target != 16S:
        #   Calculamos delta ct: (Cttarget - Ct16s)problema - (CtTarget - Ct16S)CP
        #   Ya que estamos, calculamos el log2^-deltaCt                  
    
        runs = self.spec_pcr[self.SQL_TABLES.run].unique()

        headers = [
            self.SQL_TABLES.run,
            self.SQL_TABLES.target,
            self.SQL_TABLES.cq,
            self.SQL_TABLES.sample
        ]

        data_list = []

        for run in runs:

            subset = self.spec_pcr[self.spec_pcr[self.SQL_TABLES.run] == run]
            query = self._create_query(self.SQL_TABLES.pcr_general, headers, sample_header=self.SQL_TABLES.sample,sample_id="CP")

            #Refine query:
            query = query + f" AND {self.SQL_TABLES.run} = '{run}'"

            cp_df = self._execute_query(query)
            sample_16S = self._get_cq(subset, self.KEY_16S, run)
            cp_16S = self._get_cq(cp_df, self.KEY_16S, run)

            targets = [target for target in list(subset[self.SQL_TABLES.target]) if target != self.KEY_16S]
            for target in targets:
                cq_target = self._get_cq(subset, target, run)
                cp_cq_target = self._get_cq(cp_df, target, run)



                try:
                    if cq_target == 0:
                        delta_cq = 0
                        log_cq = 0
                    else:
                        delta_cq = (cq_target - sample_16S ) - (cp_cq_target - cp_16S)
                        log_cq = np.log10(2**-delta_cq)
                except Exception as e:
                    delta_cq = np.nan
                    log_cq= np.nan
                    print(f"Error: {e}")
                
                data_dict = {
                    self.KEY_DELTA_CQ : delta_cq,
                    self.KEY_LOG_DELTA_CQ: log_cq,
                    self.SQL_TABLES.target : target,
                    self.SQL_TABLES.run : run,
                    self.KEY_CQ_16S : sample_16S,
                    self.KEY_CQ_TARGET : cq_target,
                    self.KEY_CQ_16S_CP : cp_16S,
                    self.KEY_CQ_TARGET_CP : cp_cq_target
                }

                data_list.append(data_dict)

        self.delta_cq_df = pd.DataFrame(data_list)

    def _get_cq(self, df, target, run):

        cq = df.loc[(df[self.SQL_TABLES.target] == target) &
                (df[self.SQL_TABLES.run] == run), self.SQL_TABLES.cq].values[0]
        return cq

    def get_demographics(self):#get demographic data of this sample
        pass

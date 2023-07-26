import pandas as pd
import sys
import numpy as np
from scipy.signal import  find_peaks
import matplotlib.pyplot as plt
from ..utils.constants.load_constants import SqlTables



class StudySample():
    SQL_TABLES = SqlTables()

    MIN_MELT_TEMP = 75
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

    def _create_query(self, table, headers, sample_header):
        if headers == '*':
            select_statement = '*'
        else:
            select_statement = ", ".join(headers)
        query = f"""
        SELECT {select_statement} FROM {table}
        WHERE {sample_header} = '{self.sample_id}'
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
    
    def calc_melt_temp(self, target): #Calculate melting temperature of isolate
        #TODO: Hay que arreglar la logica de este metodo y de los relacionados para almacenar correctamente la informacion

        df = self.melting_distribution

        df = df[df[self.SQL_TABLES.target] == target]

        #Select melting_range

        df = df.query(f"{self.SQL_TABLES.temperature} > {self.MIN_MELT_TEMP}")
        derivate = np.array(df[self.SQL_TABLES.melt_derivate])
        temperature = np.array(df[self.SQL_TABLES.temperature])
        #locals_max_idx = argrelmin(derivate)

        #locals_max = derivate[locals_max_idx[0]]

        filtered_peaks, threshold  = self.filter_melting_peaks(self.calc_melting_peaks(derivate), derivate)
        print(derivate.mean())
        print(derivate[filtered_peaks])
        print(temperature[filtered_peaks])
        print(filtered_peaks)
        print(temperature[filtered_peaks])

        self.plot_melt_curve(temperature, derivate, filtered_peaks, threshold)   

    def filter_melting_peaks(self, peaks, derivate_rfu, threshold_coeff = 1.7):

        if not self.check_array(derivate_rfu):
            return None
        else:
            derivate_rfu = np.array(derivate_rfu)

        threshold = threshold_coeff * derivate_rfu.mean()

        filtered_peaks = [peak for peak in peaks if derivate_rfu[peak] > threshold]

        return ( filtered_peaks, threshold)
    
    def plot_melt_curve(self, temperature, derivate, filtered_peaks, threshold, label = ''):
        plt.plot(temperature, derivate, label = label)
        plt.plot(temperature[filtered_peaks], derivate[filtered_peaks], 'ro')

        plt.axhline(threshold,linestyle = "--", color = "red")

        plt.legend()
        plt.show()
    

    def _unpack_data(self): #Unpack data of dataframes to attr. Requires duplicates management.
        pass
    def calc_delta_ct(self): #Record delta ct of specific targets
        pass
    def get_demographics(self):#get demographic data of this sample
        pass


    

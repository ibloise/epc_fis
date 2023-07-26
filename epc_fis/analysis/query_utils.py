import pandas as pd
import sys
import numpy as np
from scipy.signal import argrelmin, savgol_filter
import matplotlib.pyplot as plt
from utils.constants.load_constants import SqlTables




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
    
    def calc_melt_temp(self, target): #Calculate melting temperature of isolate
        

        df = self.melting_distribution

        df = df[df[self.SQL_TABLES.target] == target]

        #Lo escrito a continuación es una adaptación de https://notebook.community/liuyigh/PyHRM/PyHRM

        #Select melting_range

        df = df.query(f"{self.SQL_TABLES.temperature} > {self.MIN_MELT_TEMP}")
        derivate = np.array(df[self.SQL_TABLES.melt_derivate])
        temperature = np.array(df[self.SQL_TABLES.temperature])

        plt.plot(temperature, derivate, label="raw")
        plt.show()

        locals_max_idx = argrelmin(derivate)

        locals_max = derivate[locals_max_idx[0]]

        for min in locals_max:
            print(min)
            melt_temp = df.loc[df[self.SQL_TABLES.melt_derivate] == min, self.SQL_TABLES.temperature]
            print(melt_temp) #Ahora mismo encuentra los máximos en las que tienen curva correctamente, pero no discrimina las zonas de convexidad


    def _unpack_data(self): #Unpack data of dataframes to attr. Requires duplicates management.
        pass
    def calc_delta_ct(self): #Record delta ct of specific targets
        pass
    def get_demographics(self):#get demographic data of this sample
        pass


    

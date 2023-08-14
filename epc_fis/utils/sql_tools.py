import getpass
import pymysql
import re
import logging
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

class SqlConnection():

    MSG_CONNECT= 'Conectando a base de datos'

    MSG_REQUIRE_USER = 'Introduce tu usuario:'

    MSG_REQUIRE_PASSWORD = 'Introduce tu contraseña'

    MSG_CON_SUCCESS =  'Conexión creada con éxito!'

    MSG_CON_ERROR = 'No es posible conectar a base de datos'

    def __init__(self, schema, host = 'localhost', port = 3306, software='mysql'):
        self.schema = schema
        self.host = host
        self.port = port
        self.software = software
        logger.info(f'{self.MSG_CONNECT} {self.software}')

        print(self.MSG_REQUIRE_USER) #No quiero que esto vaya al logger
        self.user = input()
        logger.info(f'USER: {self.user}')

        print(self.MSG_REQUIRE_PASSWORD)
        self.password = getpass.getpass()

        self.anon_password = '*'*len(self.password)

        self.SQL_connect()

    def SQL_connect(self):
        try:
            connection = pymysql.connect(host=self.host,
                    user=self.user,
                    password=self.password,
                    port = self.port,
                    db = self.schema
                )
            logger.info(self.MSG_CON_SUCCESS)
        except Exception as e:
            logger.error(self.MSG_CON_ERROR)
            print(logger.error(e))
            exit()

        db_data = f'{self.software.lower()}+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.schema}'
        db_data_msg = re.sub(self.password, self.anon_password, db_data)

        logger.debug(f'Database create engine: {db_data_msg}')
        
        self.engine = create_engine(db_data)
        self.connection = connection
        self.cursor = connection.cursor(pymysql.cursors.DictCursor)

    def launch_table(self, dataframe, dest_table, action = 'append'):
        dataframe.to_sql(dest_table, self.engine, if_exists = action, index = False)

    def check_exist_table(self, table):
        self.cursor.execute(f"SHOW TABLES LIKE '{table}'")

        exists = self.cursor.fetchone() is not None

        return exists
    
    def close_connection(self):

        self.cursor.close()
        self.connection.close()

    def create_table_query(self, table, headers):
        if headers == '*':
            select_statement = '*'
        else:
            select_statement = ", ".join(headers)

        query = f"""
        SELECT {select_statement} FROM {table}
        """
        return query
    
    def execute_table_query(self, query):
        if not hasattr(self, 'connection'):
            logger.error("""
            Error in _execute_query: This method require connection to database. Execute StudySample.connect_db and try again
            """)
        
        df = pd.read_sql(query, self.engine)
        
        return df
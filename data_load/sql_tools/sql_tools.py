import getpass
import pymysql
import re
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

class SQL_connection():

    MSG_CONNECT= 'Conectando a base de datos'

    MSG_REQUIRE_USER = 'Introduce tu usuario:'

    MSG_REQUIRE_PASSWORD = 'Introduce tu contraseña'

    MSG_CON_SUCCESS =  'Conexión creada con éxito!'

    MSG_CON_ERROR = 'No es posible conectar a base de datos'

    def __init__(self, host = 'localhost', port = 3306, software='mysql'):

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

    def SQL_connect(self):
        try:
            connection = pymysql.connect(host=self.host,
                    user=self.user,
                    password=self.password,
                    port = self.port
                )
            logger.info(self.MSG_CON_SUCCESS)
        except Exception as e:
            logger.error(self.MSG_CON_ERROR)
            print(logger.error(e))
            exit()

        db_data = f'{self.software.lower()}+pymysql://{self.user}:{self.password}@{self.host}:{self.port}'
        db_data_msg = re.sub(self.password, self.anon_password, db_data)

        logger.debug(f'Database create engine: {db_data_msg}')
        
        self.engine = create_engine(db_data, encoding='latin1')
        self.cursor = connection.cursor(pymysql.cursors.DictCursor)

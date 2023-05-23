import sys
import os
import glob
import shutil
import pandas as pd
import logging

######QUEDA CAMBIAR LOS NA A 0!!
logger = logging.getLogger(__name__)

def group_cfx_files(cfx_path):

    logger.info(f'Reading {cfx_path}')
    files = [file for file in os.listdir(cfx_path) if os.path.isfile(os.path.join(cfx_path, file))]
    if not files:
        logger.info('No files to move!')
        return None
    #Create dictionary of runs : [files]
    runs = {}
    for file in files:
        run_id = file.split('-')[0].strip() #get run name and delete whitespaces
        runs.setdefault(run_id, []).append(file)

    for run, files in runs.items():
        if not os.path.exists(os.path.join(cfx_path, run)):
            logger.info(f'Creating {run} folder in {cfx_path}')
            os.mkdir(os.path.join(cfx_path, run))
            logger.info(f'Folder created!')
        else:
            logger.warning(f'{run} folder already exist!')

        for file in files:
            logger.info(f'Moving {file} to {os.path.join(cfx_path, run)}')
            shutil.move(os.path.join(cfx_path, file), os.path.join(cfx_path, run, file))
            logger.info(f'File moved!')

class CfxRun:

    def __init__(self, root, run_folder):

        #Paths
        self.root = root
        self.run_folder = run_folder
        self.run_path = os.path.join(root, run_folder)

            #Run information attributes
        #Sheet
        self._RUN_INFO_SHEET = 'Run Information'
        # Run info row index
        self._RUN_FILE_NAME = 'File Name'
        self._RUN_ADMIN = 'Created By User'
        self._RUN_STARTED = 'Run Started'
        self._RUN_ENDED = 'Run Ended'
        self._RUN_SAMPLE_VOL = 'Sample Vol'
        self._RUN_LID_TEMP = 'Lid Temp'
        self._RUN_PROTOCOL_FILE = 'Protocol File Name'
        self._RUN_PLATE_FILE = 'Plate Setup File Name'
        self._RUN_BASE_SERIAL = 'Base Serial Number'
        self._RUN_OPTICAL_SERIAL = 'Optical Head Serial Number'
        self._RUN_SOFTWARE_VERSION = 'CFX Maestro Version'

        #Files

        self._pattern_endpoint = 'End Point Results'
        self._pattern_melt_curve_deriv =  'Melt Curve Derivative Results'
        self._pattern_melt_curve_peaks =  'Melt Curve Peak Results'
        self._pattern_melt_curve_rfu =  'Melt Curve RFU Results'
        self._pattern_quantification_amp_results =  'Quantification Amplification Results'
        self._pattern_quantification_cq_results =  'Quantification Cq Results'

        #Tables

        self.tabulars = []

        #Headers

            #Common
        self.head_run = 'run'
        self.head_well = 'Well'
        self.head_fluor = 'Fluor'
        self.head_target = 'Target'
        self.head_sample = 'Sample'
        self.head_origin = 'origin_file'

            #EndPoint
        self.head_end_rfu = 'End RFU'

            #Melt Peak
        self.head_melt_temp = 'Melt Temperature'
        self.head_peak_height = 'Peak Height'
        self.head_begin_temp = 'Begin Temperature'
        self.head_end_temp = 'End Temperature' 

            #Cq Amp

        self.head_cq = 'Cq'

            #Melt matrixes
        self.head_temp = 'Temperature'
        self.head_melt_deriv = 'melt_derivative_value'
        self.head_melt_rfu = 'melt_rfu_value'

            #cycle matrix
        self.head_cycle = 'Cycle'
        self.head_cycle_rfu = 'cycle_rfu'

        self._core_cols = [self.head_well, self.head_sample]


    def _get_run_info_param(self, dataframe, parameter ,index = 1):
        return dataframe.loc[parameter, index]


    def create_run_info(self):
        '''
        Read one run info sheet and storage parameters
        '''
        file = os.listdir(self.run_path)[0] #Select one file
        run_info = pd.read_excel(os.path.join(self.run_path, file), sheet_name = self._RUN_INFO_SHEET,
                                 header=None, index_col=0)

        run_info.to_excel(f'{os.path.join(self.run_path, self._RUN_INFO_SHEET)}.xlsx')
        
        #set run infor parameters ?¿
        #self.run_file_name = self._get_run_info_param(run_info, self._RUN_FILE_NAME)
        #self.user = self._get_run_info_param(run_info, self._RUN_ADMIN)
        #self.run_start = self._get_run_info_param(run_info, self._RUN_STARTED)
        #self.run_ended = self._get_run_info_param(run_info, self._RUN_ENDED)
        #self.sample_vol = self._get_run_info_param(run_info, self._RUN_SAMPLE_VOL)
        #self.lid_temp = self._get_run_info_param(run_info, self._RUN_LID_TEMP)
        #self.protocol = self._get_run_info_param(run_info, self._RUN_PROTOCOL_FILE)
        #self.plate = self._get_run_info_param(run_info, self._RUN_PLATE_FILE)
        #self.base_serial_number = self._get_run_info_param(run_info, self._RUN_BASE_SERIAL)
        #self.optical_serial_number = self._get_run_info_param(run_info, self._RUN_OPTICAL_SERIAL)
        #self.manager_version = self._get_run_info_param(run_info, self._RUN_SOFTWARE_VERSION)
        self.run_info = run_info.transpose().rename(columns=self._clean_names)

    def read_config(config_file):
        pass

    def _read_file(self, file):
        logger.info(f'Reading {file}')
        try:
            data = pd.read_excel(os.path.join(self.run_path, file), usecols= lambda x: 'Unnamed' not in x)
            logging.debug(f'data readed: \n {data.to_string()}')
            data[self.head_run] = self.run_folder
            data[self.head_origin] = os.path.basename(file)
            logger.info(f'{file} readed!')
            return data
        except Exception as e:
            logger.error(f'{file} not reading!')
            logger.error(e)
            return None
        
    def _get_file(self, pattern):
        '''
        get filename for pattern
        '''
        pattern = f'*{pattern}*'
        files = glob.glob(os.path.join(self.run_path, pattern))
        logger.debug(f'Files found: {files}')
        if len(files) == 1:
            return files[0]
        elif len(files) > 1:
            logger.warning(f'Several patterns find for {pattern}. Returning first occurrence')
            return files[0]
        else:
            logger.warning(f'No files found for {pattern}')
            return None

    def read_files(self):
        '''
        Read run folder
        '''
        logging.warning('Arreglo de los screening perdidos activo! Desactivar tras primera carga')
        self.endpoint = self._read_file(self._get_file(self._pattern_endpoint))
        logging.debug(self.endpoint.to_string())
        self.melt_deriv = self._read_file(self._get_file(self._pattern_melt_curve_deriv))
        self.melt_peak = self._read_file(self._get_file(self._pattern_melt_curve_peaks))
        #fix
        self.melt_peak[self.head_target] = self.melt_peak[self.head_target].fillna('Screening')

        self.melt_rfu = self._read_file(self._get_file(self._pattern_melt_curve_rfu))
        self.quant_amp = self._read_file(self._get_file(self._pattern_quantification_amp_results))
        self.quant_cq = self._read_file(self._get_file(self._pattern_quantification_cq_results))
        #fix
        self.quant_cq[self.head_target] = self.quant_cq[self.head_target].fillna('Screening')

        self.tabulars = [self.endpoint, self.melt_peak, self.quant_cq]

        self.meltings = [self.melt_deriv, self.melt_rfu]

        self.quant_cycles = [self.quant_amp]

        self._create_tab_core()
    
    def _create_tab_core(self):
        '''
        Create a core tab necessary for create general table
        '''

        logger.warning('Create tab core method is deprecated!')
        self._tab_core = self.quant_cq[self._core_cols]
        self._tab_core = self._tab_core.drop_duplicates()

    def _check_reads(self, required):
        if not required:
            logger.error(f'Please, run {self.__class__.__name__}.read_files() before')
            sys.exit()

    def _create_subset(self, core_cols, new_cols):
        '''
        Create list of subset for self.create_general_table()
        '''
        inner_list = core_cols.copy()
        inner_list.extend(new_cols)
        return inner_list
    
    def _clean_names(self, x):
        return x.lower().replace(' ', '_')

    def create_general_table(self):
        self._check_reads(self.tabulars)

        logger.info('Creating general table')

        quant_cq_cols = self._create_subset(self._core_cols, [self.head_cq, self.head_origin])
        self.general_table = self.quant_cq[quant_cq_cols]

        #LOad End Points
        end_point_cols = self._create_subset(self._core_cols, [self.head_end_rfu, self.head_origin])
        self.general_table = self.general_table.merge(
            self.endpoint[end_point_cols],
            on = self._core_cols,
            how='left',
            suffixes=['','_end_point']
        )

        #Load melt peak
        melt_peak_cols = self._create_subset(self._core_cols, 
                            [self.head_melt_temp, self.head_peak_height, self.head_begin_temp, self.head_end_temp, self.head_origin])
        
        self.general_table = self.general_table.merge(
            self.melt_peak[melt_peak_cols],
            on=self._core_cols,
            how='left',
            suffixes=['','_melt_peak']
        )
        
        #Load quant cq

        quant_cq_cols = self._create_subset(self._core_cols, [self.head_cq, self.head_origin])

        self.general_table = self.general_table.merge(
            self.quant_cq[quant_cq_cols],
            on=self._core_cols,
            how='left',
            suffixes=['','_cq']
        )

        self.general_table = self.general_table.rename(columns=self._clean_names)

        logger.info(f'General table created!: \n {self.general_table.to_string()}')

    def unpivot_matrix(self, matrix, id_vars, value_name):
        '''
        Unpivot matrix get from cfx
        '''
        matrix = matrix.melt(
            id_vars = id_vars, var_name = self.head_well, value_name = value_name
            )
        matrix[self.head_well] = matrix[self.head_well].apply(
            lambda x :  x if (len(x) > 2) else (x[0] + "0" + x[1])
            ) #Fix discrepancies in naming wells
        return matrix
    
    def assign_samples(self, matrix):
        '''
        Assign sample names/numbers to matrix anonym wells
        '''
        matrix = matrix.merge(self._tab_core,
                            on = self.head_well,
                            how = 'left')
        return matrix
    
    def build_matrixes(self):
        
        logger.info('Managin matrixes')
        melting_id_vars = [self.head_temp, self.head_origin, self.head_run]
        unpivot_melt_deriv = self.unpivot_matrix(self.melt_deriv, id_vars= melting_id_vars,
                                                 value_name=self.head_melt_deriv)
        
        unpivot_melt_rfu = self.unpivot_matrix(self.melt_rfu, id_vars=melting_id_vars,
                                               value_name=self.head_melt_rfu)
        
        #Join the two unpivots
        unpivot_melt_data = unpivot_melt_deriv.merge(unpivot_melt_rfu, 
                                                     on=[self.head_temp, self.head_well],
                                                     suffixes=['_deriv', '_rfu'])
        
        self.unpivot_melt_data = self.assign_samples(unpivot_melt_data)
        self.unpivot_melt_data = self.unpivot_melt_data.rename(columns=self._clean_names)
        logger.info(f'Melting matrix created!: \n {self.unpivot_melt_data.to_string()}')
        #Unpivot the cycle data
        unpivot_ct = self.unpivot_matrix(self.quant_amp,
                                        id_vars=[self.head_cycle, self.head_origin, self.head_run],
                                        value_name=self.head_cycle_rfu)
        
        self.unpivot_ct = self.assign_samples(unpivot_ct)
        self.unpivot_ct = self.unpivot_ct.rename(columns=self._clean_names)
        logger.info(f'Cycle matrix created!: \n {self.unpivot_ct.to_string()}')

    def storage_run(self, storage_folder, storage_in_root = True):
        if storage_in_root:
            storage_folder = os.path.join(self.root, storage_folder)
        logger.info(f'Moving {self.run_path} to {storage_folder}')

        try:
            shutil.move(self.run_path, storage_folder)
            logger.info('Run moved!')
        except Exception as e:
            logger.error(f'Run cannot be moved! \n Exception: {e}')

    def pipeline(self):
        '''
        Run the core of the class analysis
        '''
        logger.info('Run class pipeline')
        self.create_run_info()
        self.read_files()
        self.create_general_table()
        self.build_matrixes()

#Constants

class cfxData:
        #Nota a futuro: SI hay conflicto entre versiones del CFX, configurar una variable de entrada "version" y definir las variables que cambien
        #mediante if-else en función de la versión

    #Tables
    TABLE_GENERAL = "general_data"
    TABLE_MELT = "melt_data"
    TABLE_CYCLE = "cycle_data"
    TABLE_PROJECTS = "projects"

    END_POINT = "end point"
    MELT_CURVE_DERIVATE = "melt curve derivate"
    MELT_CURVE_PEAK = "melt curve peak"
    MELT_CURVE_RFU = "melt curve rfu"
    QUANTIFICATION_AMPLIFICATION_RESULT = "quantification amplification result"
    QUANTIFICATION_CQ_RESULT = "quantification cq result"
    
    #keys
    VALUE = "value"
    KEY_REG_EXP = "regex"
    KEY_READER = "reader"
    KEY_TYPE = "type"
    KEY_DATA_SHEET = "data sheet"
    KEY_RUN_INFO_SHEET = "run info sheet"
    KEY_IMPORT_HEADERS = "import headers"
    KEY_ID_HEADER = "id headers"
    KEY_PIVOT_VALUE_HEADER = "pivot value"

    #Files Names
    END_POINT = "End Point Results"
    MELT_CURVE_DERIVATE = "Melt Curve Derivative Results"
    MELT_CURVE_PEAK = "Melt Curve Peak Results"
    MELT_CURVE_RFU = "Melt Curve RFU Results"
    QUANT_AMP_RESULT = "Quantification Amplification Results"
    QUANT_CQ_RESULT = "Quantification Cq Results"
    MELT_NOVEL_KEY = "Meltin Derivate and RFU Results"


    #Headers

    HEAD_WELL = "Well"
    HEAD_FLUOR = "Fluor"
    HEAD_TARGET = "Target"
    HEAD_SAMPLE = "Sample"
    HEAD_END_RFU = "End RFU"
    HEAD_MELT_TEMP = "Melt Temperature"
    HEAD_PEAK_HEIGHT = "Peak Height"
    HEAD_BEGIN_TEMP = "Begin Temperature"
    HEAD_END_TEMP = "End Temperature"
    HEAD_TEMPERATURE = "Temperature"
    HEAD_CYCLE = "Cycle"
    HEAD_CQ = "Cq"
    HEAD_EXCEL_FILE = "Excel file name"
    HEAD_TYPE = "data_type"
    HEAD_RUN = "run"

    HEAD_FILE_NAME  = "File Name"
    HEAD_USER = "Created By User"
    HEAD_RUN_START = "Run Started"
    HEAD_RUN_END = "Run Ended"
    HEAD_SAMPLE_VOL = "Sample Vol"
    HEAD_LID_TEMP = "Lid Temp"
    HEAD_PROTOCOL = "Protocol File Name"
    HEAD_PLATE_FILE = "Plate Setup File Name"
    HEAD_BASE_SERIAL = "Base Serial Number"
    HEAD_OPTICAL_SERIAL = "Optical Head Serial Number"
    HEAD_SOFTWARE_VERSION  = "CFX Maestro Version"
    HEAD_PIVOT_MELT_DERIVATE = "melt_derivate"
    HEAD_PIVOT_MELT_RFU = "melt_rfu"
    HEAD_PIVOT_CYCLE_RFU = "cycle_RFU"

    #Options:

    LONG_FORMAT = "long format"
    MATRIX_FORMAT = "matrix format"
    SYBR = "SYBR"
    ZERO = "0"
    RUN_INFO = "Run Information"

    cfx_files_features = {
        END_POINT: {
            KEY_REG_EXP : END_POINT,
            KEY_READER : True,
            KEY_TYPE : LONG_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_IMPORT_HEADERS : [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_END_RFU]
        },
        MELT_CURVE_DERIVATE: {
            KEY_REG_EXP : MELT_CURVE_DERIVATE,
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_TEMPERATURE],
            KEY_PIVOT_VALUE_HEADER: HEAD_PIVOT_MELT_DERIVATE

        },
        MELT_CURVE_PEAK: {
            KEY_REG_EXP : MELT_CURVE_PEAK,
            KEY_READER : True,
            KEY_TYPE : LONG_FORMAT,
            KEY_DATA_SHEET : ZERO,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_IMPORT_HEADERS : [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_MELT_TEMP, HEAD_PEAK_HEIGHT, HEAD_BEGIN_TEMP, HEAD_END_TEMP]
        },
        MELT_CURVE_RFU: {
            KEY_REG_EXP : MELT_CURVE_RFU,
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_TEMPERATURE],
            KEY_PIVOT_VALUE_HEADER: HEAD_PIVOT_MELT_RFU
        },
        QUANTIFICATION_AMPLIFICATION_RESULT: {
            KEY_REG_EXP : QUANT_AMP_RESULT,
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_CYCLE],
            KEY_PIVOT_VALUE_HEADER : HEAD_PIVOT_CYCLE_RFU

        },
        QUANTIFICATION_CQ_RESULT: {
            KEY_REG_EXP : QUANT_CQ_RESULT ,
            KEY_READER : True,
            KEY_TYPE : LONG_FORMAT,
            KEY_DATA_SHEET : ZERO,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_IMPORT_HEADERS : [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_CQ]
        }
    }

class microbData:
    #Tables
    PATIENT_TABLE = "patients"
    SAMPLE_TABLE = "samples"
    RESULTS_TABLE = "results"
    CARBA_TABLE = "carba"

    #fields
    HEAD_NHC = "nºhistoria"
    HEAD_CIPA = "afi"
    HEAD_LASTNAME_1 = "Apellido1"
    HEAD_LASTNAME_2 = "Apellido2"
    HEAD_NAME = "Nombre"
    HEAD_SEX = "Sexo"
    HEAD_DBIRTH = "Fec.Nacimiento"
    HEAD_NSAMPLE = "NºMuestra"
    HEAD_DENTRY = "Fec.Entrada"
    HEAD_DRESULT = "Fec.Resultado"
    HEAD_COD_GFH = "Cod.Procedencia"
    HEAD_DES_GFH = "Des.Procedencia"
    HEAD_SAMPLE_TYPE = "Des.Muestra"
    HEAD_MO = "Des.Microorganismo"
    HEAD_RESULT = "Cod.Observaciones.1"
    HEAD_DES_RESULT = "Des.Resultado"

    #Miscellaneous
    MICROB_DELIM = "|"
    VALUE_CARBA = "CBP"
    VALUE_OXA = "OXA"
    VALUE_VIM = "VIM"
    VALUE_KPC = "KPC"
    VALUE_NDM = "NDM"
    VALUE_BLEE = "BLE"
    VALUE_ANT = "ANT"
    VALUE_NEGATIVE = "Negativo"
    VALUE_PENDING  = "PENDIENTE DE RESULTADO"
    OXA_48 = "oxa48"
    VIM = "vim"
    KPC = "kpc"
    NDM = "ndm"
    BLEE = "esbl"
    CARBA = "carbapenemasa"
    ANT = "Caracterizado en anterior"

    #Lists
    USE_COLS = [HEAD_NHC,
            HEAD_CIPA,
            HEAD_LASTNAME_1,
            HEAD_LASTNAME_2,
            HEAD_NAME,
            HEAD_SEX,
            HEAD_DBIRTH,
            HEAD_NSAMPLE,
            HEAD_DENTRY,
            HEAD_DRESULT,
            HEAD_COD_GFH,
            HEAD_DES_GFH,
            HEAD_SAMPLE_TYPE,
            HEAD_MO,
            HEAD_RESULT,
            HEAD_DES_RESULT
    ]

    COLS_SUB_PATIENTS = [HEAD_NHC,
                     HEAD_CIPA,
                     HEAD_LASTNAME_1,
                     HEAD_LASTNAME_2,
                     HEAD_NAME,
                     HEAD_SEX,
                     HEAD_DBIRTH
    ]

    COLS_SUB_SAMPLE = [HEAD_NHC,
                   HEAD_NSAMPLE,
                   HEAD_DENTRY,
                   HEAD_DRESULT,
                   HEAD_COD_GFH,
                   HEAD_DES_GFH,
                   HEAD_SAMPLE_TYPE
    ]

    COLS_SUB_RESULTS = [HEAD_NSAMPLE,
                    HEAD_MO
    ]

    COLS_SUB_CARBADATA = [
         HEAD_NSAMPLE, 
         HEAD_MO,
         HEAD_RESULT
    ]


    VALUES_PIVOT = [VALUE_OXA, 
                VALUE_KPC, 
                VALUE_NDM, 
                VALUE_VIM, 
                VALUE_ANT, 
                VALUE_BLEE, 
                VALUE_CARBA
    ]
    #Dicts
    SUBSETS = {
    PATIENT_TABLE : COLS_SUB_PATIENTS,
    SAMPLE_TABLE : COLS_SUB_SAMPLE,
    RESULTS_TABLE :  COLS_SUB_RESULTS,
    CARBA_TABLE :  COLS_SUB_CARBADATA
    }

    CONVERTER = {VALUE_OXA: OXA_48,
                VALUE_VIM :VIM,
                VALUE_KPC: KPC,
                VALUE_NDM : NDM,
                VALUE_BLEE: BLEE,
                VALUE_CARBA: CARBA,
                VALUE_ANT: ANT }
    

class sqlLoader:
    #Variables

    SQL_STRUCTURE_KEY = "SQL_STRUCTURE"
    COLS_KEY = "cols"
    SOURCES_KEY = "sources"
    SQL_COMPOSITE = "sql_composite"
    REQUIRE_KEY = "table_requirements"

    #SCHEMA
    FIS_SCHEMA = "FIS_EPC"
    TEST_SCHEMA = "FIS_EPC_TEST_ZONE"

    #Origins:

    MICROB = "microb"
    CFX = "cfx"
    SERVOLAB = "servolab"
    SAVANA = "savana"

    SOURCES = {
        MICROB : microbData,
        CFX :  cfxData,
        SERVOLAB : "",
        SAVANA : ""
    }

    #messages
    MSG_CONNECT  = "Conectando a MySQL"
    MSG_USER = "Introduce el usuario:"
    MSG_PASS = "Introduce tu contraseña:"
    MSG_SUCCESS = "Conexión establecida!"
    MSG_CONNECT_ERROR = "No se ha podido establecer la conexión con MySQL. El proceso se ha abortado"

     #Tables
        #Microb
    TABLE_PATIENTS = "patients"
    TABLE_SAMPLES = "samples"
    TABLE_RESULTS = "results"
    TABLE_CARBA = "carba"
    TABLE_CODMO = "mocodif"
    TABLE_GFH = "GFH"

        #pcr
    TABLE_PCR = "pcr"
    TABLE_MELTING = "melting"
    TABLE_CYCLES = "cycles"
    TABLE_PROJECTS = "projects"

    #Headers
        #Patients
    HEAD_NHC = "nhc"
    HEAD_CIPA = "cipa"
    HEAD_NAME = "name"
    HEAD_LASTNAME = "lastname"
    HEAD_BIRTHDATE = "birth_date"
    HEAD_SEX = "sex"

        #samples
    HEAD_SAMPLE = "sampleid"
    HEAD_SAMPLE_TYPE = "sample_type"
    HEAD_ENTRY = "entry_date"
    HEAD_RESULTDATE = "result_date"
    HEAD_GFH = "cod_gfh"

        #results
    HEAD_RESULT = "result"

        #carbas
    HEAD_CARBA = "carba"

        #pcr
    HEAD_WELL = "well"
    HEAD_FLUOR = "fluor"
    HEAD_TARGET = "target"
    HEAD_RFU = "end_rfu"
    HEAD_RUN = "run"
    HEAD_MELT = "mel_temperature"
    HEAD_PEAK = "peak_height"
    HEAD_BEGIN_TEMP = "begin_temperature"
    HEAD_END_TEMP = "end_temperature"
    HEAD_CT = "ct"

        #projects
    HEAD_FILENAME = "filename"
    HEAD_USER = "user"
    HEAD_RUN_START = "run_started"
    HEAD_RUN_END = "run_ended"
    HEAD_SAMPLE_VOL = "sample_vol"
    HEAD_LID_TEMP = "lid_temp"
    HEAD_PROTOCOL_FILE = "protocol_filename"
    HEAD_PLATE_FILE = "plate_file"
    HEAD_BASE_SERIAL = "base_serial_number"
    HEAD_OPTICAL_SERIAL = "optical_serial_number"
    HEAD_SOFTWARE_VERSION = "software_v"

    #melting
    HEAD_TEMPERATURE = "temperature"
        #HEAD_WELL
    HEAD_MELT_DERIVATE = "melt_derivate"
        #HEAD_RUN
        #HEAD_SAMPLE
    HEAD_MELT_RFU = "melt_rfu"

    #excel
    HEAD_EXCEL_FILE = "excel_filename"

    #Tables

    TABLES = {
        TABLE_PATIENTS : {
            COLS_KEY: {
                            HEAD_NHC : {
                                SQL_STRUCTURE_KEY : "VARCHAR(15) PRIMARY KEY NOT NULL",
                                MICROB : [SOURCES[MICROB].HEAD_NHC]},
                            HEAD_CIPA : {
                                SQL_STRUCTURE_KEY : "VARCHAR(15)",
                                MICROB : [SOURCES[MICROB].HEAD_CIPA]
                            },
                            HEAD_NAME : {
                                SQL_STRUCTURE_KEY : "VARCHAR(15)",
                                MICROB : [SOURCES[MICROB].HEAD_NAME]
                          },
                          HEAD_LASTNAME:{
                                SQL_STRUCTURE_KEY : "VARCHAR(15)",
                                MICROB : [SOURCES[MICROB].HEAD_LASTNAME_1, SOURCES[MICROB].HEAD_LASTNAME_2]
                          },
                          HEAD_BIRTHDATE : {
                                SQL_STRUCTURE_KEY : "DATE NOT NULL",
                                MICROB : [SOURCES[MICROB].HEAD_DBIRTH]
                          },
                          HEAD_SEX : {
                                SQL_STRUCTURE_KEY : "CHAR(5)",
                                MICROB : [SOURCES[MICROB].HEAD_SEX]
                          }
            },
            SQL_COMPOSITE : "",
            REQUIRE_KEY : [],
            SOURCES_KEY: {
                MICROB: [SOURCES[MICROB].PATIENT_TABLE]
            }
        },
        TABLE_SAMPLES : {
            COLS_KEY : {
                        HEAD_NHC : {
                            SQL_STRUCTURE_KEY : "VARCHAR(15) NOT NULL", 
                            MICROB : [SOURCES[MICROB].HEAD_NHC]
                        },
                        HEAD_SAMPLE : {
                            SQL_STRUCTURE_KEY : "VARCHAR(15) PRIMARY KEY NOT NULL",
                            MICROB : [SOURCES[MICROB].HEAD_NSAMPLE]
                         },
                        HEAD_SAMPLE_TYPE : {
                            SQL_STRUCTURE_KEY : "VARCHAR(10) NOT NULL",
                            MICROB : [SOURCES[MICROB].HEAD_SAMPLE_TYPE]
                        },
                        HEAD_ENTRY : {
                            SQL_STRUCTURE_KEY : "DATE NOT NULL",
                            MICROB : [SOURCES[MICROB].HEAD_DENTRY]
                         },
                        HEAD_RESULTDATE : {
                            SQL_STRUCTURE_KEY : "DATE NOT NULL",
                            MICROB : [SOURCES[MICROB].HEAD_DRESULT]
                         },
                        HEAD_GFH : {
                            SQL_STRUCTURE_KEY : "VARCHAR(10)",
                            MICROB :[SOURCES[MICROB].HEAD_COD_GFH]
                         }
            },
            SQL_COMPOSITE : f"FOREIGN KEY ({HEAD_NHC}) REFERENCES {TABLE_PATIENTS}({HEAD_NHC})",
            REQUIRE_KEY : [TABLE_PATIENTS],
            SOURCES_KEY: {
                MICROB:SOURCES[MICROB].SAMPLE_TABLE
            }
        },
        TABLE_RESULTS : {
            COLS_KEY: {
                        HEAD_SAMPLE : {
                            SQL_STRUCTURE_KEY : "VARCHAR (15)",
                            MICROB : [SOURCES[MICROB].HEAD_NSAMPLE]
                        } ,
                         HEAD_RESULT : {
                            SQL_STRUCTURE_KEY : "VARCHAR (20)",
                            MICROB : [SOURCES[MICROB].HEAD_MO]
                         }
            },
            SQL_COMPOSITE : "",
            REQUIRE_KEY : [],
            SOURCES_KEY: {
                MICROB: [SOURCES[MICROB].RESULTS_TABLE]
            }
        },
        TABLE_CARBA : {
            COLS_KEY : {
                        HEAD_SAMPLE : {
                            SQL_STRUCTURE_KEY : "VARCHAR(15)",
                            MICROB : [SOURCES[MICROB].HEAD_NSAMPLE]
                        } ,
                        HEAD_RESULT : {
                        SQL_STRUCTURE_KEY : "VARCHAR(15)",
                        MICROB : [SOURCES[MICROB].HEAD_MO]
                         },
                       HEAD_CARBA : {
                        SQL_STRUCTURE_KEY : "VARCHAR(10)",
                        MICROB : [SOURCES[MICROB].HEAD_RESULT]
                       }
            },
            SQL_COMPOSITE : f"PRIMARY KEY ({HEAD_SAMPLE}, {HEAD_RESULT}), FOREIGN KEY ({HEAD_SAMPLE}) REFERENCES {TABLE_SAMPLES}({HEAD_SAMPLE})",
            REQUIRE_KEY : [TABLE_SAMPLES],
            SOURCES_KEY: {
                MICROB: [SOURCES[MICROB].CARBA_TABLE]
            }
        },
        TABLE_PROJECTS : {
            COLS_KEY : {
                        HEAD_FILENAME : {
                            SQL_STRUCTURE_KEY : "VARCHAR (15) PRIMARY KEY",
                            CFX : [SOURCES[CFX].HEAD_FILE_NAME]
                            },
                          HEAD_USER : {
                            SQL_STRUCTURE_KEY : "VARCHAR(10)",
                            CFX : [SOURCES[CFX].HEAD_USER]
                          },
                          HEAD_RUN_START : {
                            SQL_STRUCTURE_KEY : "DATETIME",
                            CFX : [SOURCES[CFX].HEAD_RUN_START]
                          },
                          HEAD_RUN_END : {
                            SQL_STRUCTURE_KEY : "DATETIME",
                            CFX : [SOURCES[CFX].HEAD_RUN_END]
                          },
                          HEAD_SAMPLE_VOL : {
                            SQL_STRUCTURE_KEY : "VARCHAR(10)",
                            CFX : [SOURCES[CFX].HEAD_SAMPLE_VOL]
        
                          },
                          HEAD_LID_TEMP  : {
                            SQL_STRUCTURE_KEY : "INT",
                            CFX : [SOURCES[CFX].HEAD_LID_TEMP]
                          },
                          HEAD_PROTOCOL_FILE : {
                            SQL_STRUCTURE_KEY : "VARCHAR(100)",
                            CFX : [SOURCES[CFX].HEAD_PROTOCOL]
                          },
                          HEAD_PLATE_FILE : {
                            SQL_STRUCTURE_KEY : "VARCHAR(100)",
                            CFX : [SOURCES[CFX].HEAD_PLATE_FILE]
                          },
                          HEAD_BASE_SERIAL : {
                            SQL_STRUCTURE_KEY : "VARCHAR(15)",
                            CFX : [SOURCES[CFX].HEAD_BASE_SERIAL]
                          },
                          HEAD_OPTICAL_SERIAL : {
                            SQL_STRUCTURE_KEY : "VARCHAR (15)",
                            CFX : [SOURCES[CFX].HEAD_OPTICAL_SERIAL]
                          },
                          HEAD_SOFTWARE_VERSION : {
                            SQL_STRUCTURE_KEY : "VARCHAR(15)",
                            CFX : [SOURCES[CFX].HEAD_SOFTWARE_VERSION]
                          }
            },
            SQL_COMPOSITE : "",
            REQUIRE_KEY : [],
            SOURCES_KEY: {
                CFX: SOURCES[CFX].TABLE_PROJECTS
            }
        },
        TABLE_PCR : {
            COLS_KEY : {
                    HEAD_WELL : {
                        SQL_STRUCTURE_KEY : "VARCHAR(3)",
                        CFX : [SOURCES[CFX].HEAD_WELL]
                    },
                     HEAD_FLUOR : { 
                        SQL_STRUCTURE_KEY : "VARCHAR(10)",
                        CFX : [SOURCES[CFX].HEAD_FLUOR]
                     },
                     HEAD_TARGET :  {
                        SQL_STRUCTURE_KEY : "VARCHAR(10)",
                        CFX : [SOURCES[CFX].HEAD_TARGET]
                     },
                     HEAD_SAMPLE : {
                        SQL_STRUCTURE_KEY : "VARCHAR(15) NOT NULL",
                        CFX : [SOURCES[CFX].HEAD_SAMPLE]
                     },
                     HEAD_RFU : {
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_END_RFU]
                     },
                     HEAD_RUN : {
                        SQL_STRUCTURE_KEY : "VARCHAR (30) NOT NULL",
                        CFX : [SOURCES[CFX].HEAD_RUN]
                     },
                     HEAD_MELT : { 
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_MELT_TEMP]
                     },
                     HEAD_PEAK : {
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_PEAK_HEIGHT]
                     },
                     HEAD_BEGIN_TEMP : {
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_BEGIN_TEMP]
                     },
                     HEAD_END_TEMP : {
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_END_TEMP]
                     },
                     HEAD_CT : {
                        SQL_STRUCTURE_KEY : "INT",
                        CFX : [SOURCES[CFX].HEAD_CQ]
                     }
            },
            SQL_COMPOSITE : (f"PRIMARY KEY ({HEAD_WELL}, {HEAD_SAMPLE}, {HEAD_RUN}), " 
            f"FOREIGN KEY ({HEAD_SAMPLE}) REFERENCES {TABLE_SAMPLES}({HEAD_SAMPLE}), "
            f"FOREIGN KEY ({HEAD_RUN}) REFERENCES {TABLE_PROJECTS}({HEAD_FILENAME})"),
            REQUIRE_KEY : [TABLE_SAMPLES, TABLE_PROJECTS],
            SOURCES_KEY: {
                CFX: SOURCES[CFX].TABLE_GENERAL
            },   
        },
        TABLE_MELTING:{
            COLS_KEY: {
                    HEAD_TEMPERATURE:{
                        SQL_STRUCTURE_KEY: "INT",
                        CFX: [SOURCES[CFX].HEAD_TEMPERATURE]
                    },
                    HEAD_WELL:{
                        SQL_STRUCTURE_KEY: "VARCHAR(5) NOT NULL",
                        CFX: [SOURCES[CFX].HEAD_WELL]
                    },
                    HEAD_MELT_DERIVATE:{
                        SQL_STRUCTURE_KEY: "INT",
                        CFX: [SOURCES[CFX].HEAD_PIVOT_MELT_DERIVATE]
                    },
                    HEAD_RUN: {
                        SQL_STRUCTURE_KEY: "VARCHAR(30) NOT NULL",
                        CFX: [SOURCES[CFX].HEAD_RUN]
                    },
                    HEAD_SAMPLE: {
                        SQL_STRUCTURE_KEY: "VARCHAR(15) NOT NULL",
                        CFX: [SOURCES[CFX].HEAD_SAMPLE]
                    },
                    HEAD_MELT_RFU: {
                        SQL_STRUCTURE_KEY: "INT",
                        CFX: [SOURCES[CFX].HEAD_PIVOT_MELT_RFU]
                    }
                },
                SQL_COMPOSITE: (f"PRIMARY KEY ({HEAD_WELL}, {HEAD_SAMPLE}, {HEAD_RUN}, {HEAD_TEMPERATURE}), "
                                    f"FOREIGN KEY ({HEAD_SAMPLE}) REFERENCES {TABLE_SAMPLES} ({HEAD_SAMPLE}), "
                                    f"FOREIGN KEY ({HEAD_RUN}) REFERENCES {TABLE_PROJECTS} ({HEAD_FILENAME})"),
                REQUIRE_KEY: [TABLE_SAMPLES, TABLE_PROJECTS],
                SOURCES_KEY: {
                            CFX: SOURCES[CFX].MELT_NOVEL_KEY
                }
        }
    }


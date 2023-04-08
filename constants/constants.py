#Constants

#Miscellaneous

class folderManager():
        FOLDER_SEP = "/"

#Keys

class cfxData:
    END_POINT = "end point"
    MELT_CURVE_DERIVATE = "melt curve derivate"
    MELT_CURVE_PEAK = "melt curve peak"
    MELT_CURVE_RFU = "melt curve rfu"
    QUANTIFICATION_AMPLIFICATION_RESULT = "quantification amplification result"
    QUANTIFICATION_CQ_RESULT = "quantification cq result"

    KEY_REG_EXP = "regex"
    KEY_READER = "reader"
    KEY_TYPE = "type"
    KEY_DATA_SHEET = "data sheet"
    KEY_RUN_INFO_SHEET = "run info sheet"
    KEY_IMPORT_HEADERS = "import headers"
    KEY_ID_HEADER = "id headers"
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
#Options:

    LONG_FORMAT = "long format"
    MATRIX_FORMAT = "matrix format"
    SYBR = "SYBR"
    ZERO = "0"
    RUN_INFO = "Run Information"

    cfx_files_features = {
        END_POINT: {
            KEY_REG_EXP : "End Point Results",
            KEY_READER : True,
            KEY_TYPE : LONG_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_IMPORT_HEADERS : [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_END_RFU]
        },
        MELT_CURVE_DERIVATE: {
            KEY_REG_EXP : "Melt Curve Derivative Results",
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_TEMPERATURE]

        },
        MELT_CURVE_PEAK: {
            KEY_REG_EXP : "Melt Curve Peak Results",
            KEY_READER : True,
            KEY_TYPE : LONG_FORMAT,
            KEY_DATA_SHEET : ZERO,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_IMPORT_HEADERS : [HEAD_WELL, HEAD_FLUOR, HEAD_TARGET, HEAD_SAMPLE, HEAD_MELT_TEMP, HEAD_PEAK_HEIGHT, HEAD_BEGIN_TEMP, HEAD_END_TEMP]
        },
        MELT_CURVE_RFU: {
            KEY_REG_EXP : "Melt Curve RFU Results",
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_TEMPERATURE]
        },
        QUANTIFICATION_AMPLIFICATION_RESULT: {
            KEY_REG_EXP : "Quantification Amplification Results",
            KEY_READER : True,
            KEY_TYPE : MATRIX_FORMAT,
            KEY_DATA_SHEET : SYBR,
            KEY_RUN_INFO_SHEET : RUN_INFO,
            KEY_ID_HEADER : [HEAD_CYCLE]
        },
        QUANTIFICATION_CQ_RESULT: {
            KEY_REG_EXP : "Quantification Cq Results",
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

    #Miscellaneous
    MICROB_DELIM = "|"
    VALUE_CARBA = "CBP"
    VALUE_OXA = "OXA"
    VALUE_VIM = "VIM"
    VALUE_KPC = "KPC"
    VALUE_NDM = "NDM"
    VALUE_BLEE = "BLE"
    VALUE_ANT = "ANT"
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
            HEAD_RESULT
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
#Constants

#Miscellaneous

FOLDER_SEP = "/"

#Keys

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
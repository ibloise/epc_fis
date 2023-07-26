from utils.sql_tools import SqlConnection
import numpy as np
from scipy.signal import  find_peaks
import matplotlib.pyplot as plt
from query_utils import StudySample


sample = "062045206"

study_sample = StudySample(sample)

sql_connection = SqlConnection('fis_data_temp')

study_sample.connect_db(sql_connection)

study_sample.get_screening()

study_sample.get_spec()

study_sample.get_melting()

df = study_sample.melting_distribution

print(df)
target = "OXA48"

study_sample.calc_melt_temp(target)

exit()

df = df.query("target == @target")

#df = df.query(f'temperature >= {analytical_range[0]} and temperature <= {analytical_range[1]}')

#Vamos con media movil


derivate = np.array(df["melt_derivative_value"])
temperature = np.array(df["temperature"])

def check_array(np_array):
    try:
        np_array = np.array(np_array)
        return True
    except Exception as e:
        print("Object derivate_rfu must be a numpy array or convertible to one.")
        print("Error:")
        print(e)
        return False


def calc_melting_peaks(derivate_rfu, mode = "multimodal"):
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

    if not check_array(derivate_rfu):
        return None
 
    if mode == "multimodal":
        peaks, _ = find_peaks(derivate_rfu, distance=1)
    elif mode == "unimodal":
        peaks = [int(np.argmax(derivate_rfu))]
    else:
        print("ERROR: mode argument only accepts unimodal or multimodal")
        return None

    return peaks

def filter_melting_peaks(peaks, derivate_rfu, threshold_coeff = 1.7):

    if not check_array(derivate_rfu):
        return None
    else:
        derivate_rfu = np.array(derivate_rfu)

    threshold = threshold_coeff * derivate_rfu.mean()

    filtered_peaks = [peak for peak in peaks if derivate_rfu[peak] > threshold]

    

    return ( filtered_peaks, threshold)

    

plt.plot(temperature, derivate, label = "original")


filtered_peaks, threshold = filter_melting_peaks(calc_melting_peaks(derivate), derivate)


print(derivate.mean())
print(derivate[filtered_peaks])
print(temperature[filtered_peaks])




plt.plot(temperature[filtered_peaks], derivate[filtered_peaks], 'ro')

plt.axhline(threshold,linestyle = "--", color = "red")

plt.legend()
plt.show()


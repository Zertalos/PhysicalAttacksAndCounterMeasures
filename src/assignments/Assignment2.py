import math
import numpy as np
from src.framework.csv_reader import Csv_Reader as cr
from src.assignments import Assignment2
from assignemntconfig import AssignmentConfigManager as config
from src.framework.sbox import aes_sbox
from src.framework.DiagramHandler import Diagram_Drawer
from multiprocessing import Pool
from scipy.stats import ttest_ind
from timeit import default_timer as timer

config.get_instance("Assignment 2")
reader = None

def testkey(selected_byte, key):
    selected_byte = selected_byte ^ key
    return aes_sbox(selected_byte)

def calc_t(mean0,mean1,s0,s1,n0,n1):
    zähler = mean0-mean1
    part1 = s0**2/n0
    part2 = s1**2/n0
    sum_sqrt = part1 + part2
    nenner = math.sqrt(sum_sqrt)
    result = zähler / nenner
    return result

def process_byte(byte, reader):
    print(f'Processing byte {byte}.')
    keyresults = np.zeros(256)
    plain_text_bytes = reader.data[:, byte:byte + 1].T.ravel()
    for key in range(256):
        print(f'  Processing key-guess {byte:02} ->  {key}')
        results = np.vectorize(testkey)(plain_text_bytes, key)
        msb = (results & 128) // 128
        group_0 = reader.plaintext_timings[np.where(msb == 0)]
        group_1 = reader.plaintext_timings[np.where(msb == 1)]

        mean0 = np.mean(group_0)
        mean1 = np.mean(group_1)
        t_stat, p_value = ttest_ind(group_0, group_1)
        t_value = abs(t_stat)
        #t = calc_t(mean0=mean0,
        #           mean1=mean1,
        #           s0=np.var(group_0),
        #           s1=np.var(group_1),
        #           n0=len(group_0),
        #           n1=len(group_1))
        #
        keyresults[key] = t_value
    max_diff = np.max(keyresults)
    max_id = np.argmax(keyresults)

    dd: Diagram_Drawer = Diagram_Drawer(data=[keyresults,[4.5]*256,[-4.5]*256])
    dd.config.update({
        "plot_title": f'Key search for Byte {byte}, data points: {len(reader.data)}',
        "plot_to_display": False,
        "plot_to_disk": True,
        "x_label": "Key value in binary",
        "y_label": "t-Value",
        "plot_annotation_at": {0: [(max_id, round(max_diff, 2)), f'Maximum at ({max_id}, {round(max_diff, 2)})']},
        "plot_output_name": f"plot_k_t_{byte:02}.png",
        "plot_line_colors": ['tab:red', 'tab:blue', 'tab:red']
    })
    dd.data_to_plot()
    print(f"Byte {byte} finished.")
    return max_id

BYTES_TO_CALC = 16
def parallel(reader):
    with Pool() as pool:
        results = pool.starmap(process_byte, [(b, reader) for b in range(BYTES_TO_CALC)])
    print(f" => Found Key: {results}")

def sequential(reader):
    results = [0] * BYTES_TO_CALC
    for byte in range(0,BYTES_TO_CALC):
        results[byte] = process_byte(byte,reader)
    print(f" => Found Key: {results}")

def start():
    global reader
    print("Start reading CSV. May take a while...")
    start_csv = timer()
    reader = cr(filename="Timing_Noisy .csv")
    end_csv = timer()
    print("CSV reading done.")
    start_key = timer()
    parallel(reader=reader)
    end_key = timer()
    print(f"Time to load CSV: {end_csv - start_csv:.2f}")
    print(f"Time to find key: {end_key - start_key:.2f}")

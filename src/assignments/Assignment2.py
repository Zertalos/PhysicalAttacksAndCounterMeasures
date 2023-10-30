import math
import numpy as np
from src.framework.csv_reader import Csv_Reader as cr
from src.assignments import Assignment2
from assignemntconfig import AssignmentConfigManager as config
from src.framework.sbox import aes_sbox
from src.framework.DiagramHandler import Diagram_Drawer
from multiprocessing import Pool

config.get_instance("Assignment 2")
reader = None

def testkey(selected_byte, key):
    selected_byte = selected_byte ^ key
    return aes_sbox(selected_byte)

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
        keyresults[key] = abs(np.mean(group_0) - np.mean(group_1))

    max_diff = np.max(keyresults)
    max_id = np.argmax(keyresults)
    dd: Diagram_Drawer = Diagram_Drawer(data=[keyresults])
    dd.config.update({
        "plot_title": f'Key search for Byte {byte}, data points: {len(reader.data)}',
        "plot_to_display": False,
        "plot_to_disk": True,
        "x_label": "Key value in binary",
        "y_label": "Difference of group 1 and group 0",
        "plot_annotation_at": [[(max_id, round(max_diff, 2)), f'Maximum at ({max_id}, {round(max_diff, 2)})']],
        "plot_output_name": f"plot_k_t_{byte:02}.png"
    })
    dd.data_to_plot()
    print(f"Byte {byte} finished.")
    return byte

def start():
    global reader
    print("Start reading CSV. May take a while...")
    reader = cr(filename="Timing_Noisy.csv")
    print("CSV reading done.")
    with Pool() as pool:
        pool.starmap(process_byte, [(b, reader) for b in range(16)])
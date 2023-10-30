###
#
# Assignment_1 solution for PAC
# Christian Werner Heß - 1996650
#
##
from typing import List, Tuple
import struct


class Trace_Reader:
    """
    This class is designed to read power traces from a binary file.
    The power traces are stored in a specific format:
    - The number of points in a trace (4 bytes, unsigned int)
    - The power measurements (1 byte per measurement, signed int)

    Attributes:
    filename (str): The path to the binary file containing the power traces.
    power_measurement_count (int): The number of power measurements in the file.
    """

    def __init__(self, filename: str, power_measurement_count: int):
        """
        Initializes a new TraceReader object.

        Args:
        filename (str): The path to the binary file containing the power traces.
        power_measurement_count (int): The number of power measurements in the file.

        Raises:
        ValueError: If filename is an empty string or if power_measurement_count is less than 1.
        """
        if not filename:
            raise ValueError("filename cannot be an empty string")
        if power_measurement_count < 1:
            raise ValueError("power_measurement_count must be at least 1")

        self.filename = filename
        self.power_measurement_count = power_measurement_count

    def read_traces(self) -> List[Tuple[int, ...]]:
        """
        Reads the power traces from the binary file.

        Returns:
        List[Tuple[int, ...]]: A list of tuples, where each tuple represents a power trace.
        """
        with open(self.filename, 'rb') as f:
            data = f.read()

        traces = []
        offset = 0
        for _ in range(self.power_measurement_count):  # There are X traces per file
            # Read the number of points (uint32)
            nr_of_points = struct.unpack_from('<I', data, offset)[0]
            offset += 4

            # Read the power measurements (int8)
            trace = struct.unpack_from(f'<{nr_of_points}b', data, offset)
            traces.append(trace)
            offset += nr_of_points

        return traces

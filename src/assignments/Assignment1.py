from src.framework.TraceReader import Trace_Reader
from src.framework.DiagramHandler import Diagram_Drawer
from assignemntconfig import AssignmentConfigManager, AssignmentConfig


def plot_trace_data(filename: str, plot_title: str, output_name: str, plot_line_labels,
                    power_measurement_count: int = 5):
    tp = Trace_Reader(filename=filename, power_measurement_count=power_measurement_count)
    trace_data = tp.read_traces()

    dd = Diagram_Drawer(data=trace_data)
    dd.config.update({
        "plot_title": plot_title,
        "plot_output_name": output_name,
        "plot_line_labels": plot_line_labels
    })
    dd.data_to_plot()


AssignmentConfigManager.get_instance("Assignment 1")
plot_line_labels = [f"Trace {i + 1}" for i in range(0, 5)]

plot_trace_data(
    filename="input/Assignment_1/Traces_A.dat",
    plot_title="Plots from Traces A",
    output_name="Trace_A_plot.png",
    plot_line_labels=plot_line_labels,
    power_measurement_count=5
)

plot_trace_data(
    filename="input/Assignment_1/Traces_B.dat",
    plot_title="Plots from Traces B",
    output_name="Trace_B_plot.png",
    plot_line_labels=plot_line_labels,
    power_measurement_count=5
)

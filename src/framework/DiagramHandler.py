import matplotlib.pyplot as plot
from assignemntconfig import AssignmentConfig, AssignmentConfigManager


class Diagram_Drawer:
    """
    A class for drawing and managing diagrams using Matplotlib.

    Attributes:
        figure (matplotlib.figure.Figure): The main figure object for the diagram.
        data (list): The dataset to be plotted.
        _config (dict): A dictionary to store configuration settings for the plot.

    Methods:
        config: A property that returns the current configuration settings.
        data_to_plot: Manages the plotting process based on the configuration settings.
        plot_setup: Sets up the main figure and its title.
        plot_data_processing: Handles the data plotting and line styling.
        plot_to_file: Saves the current plot to a file.
        plot_to_display: Displays the plot on the screen.
    """

    def __init__(self, data, config=None):
        """
        Initializes a new instance of the DiagramDrawer class.

        Args:
            data (list): The dataset to be plotted.
            config (dict, optional): A dictionary of configuration settings for the plot. If not provided,
                                     a default configuration is used.

        Configuration Dictionary Keys:
            plot_title (str): The main title of the plot.
            y_label (str): The label for the Y-axis.
            x_label (str): The label for the X-axis.
            data_title (list): Titles for each dataset (not used in the current implementation).
            plot_size (tuple): The size of the plot in inches.
            plot_output_name (str): The name of the output file when saving the plot.
            plot_output_folder (str): The directory path for saving the output plot file.
            plot_to_display (bool): A flag to determine whether to display the plot on the screen.
            plot_to_disk (bool): A flag to determine whether to save the plot to a file.
            plot_line_colors (list): A list of colors for the lines in the plot.
            plot_line_labels (list): A list of labels for the lines in the plot.
            plot_enable_legend (bool): A flag to determine whether to display the legend on the plot.
        """
        self.figure = None
        if config is not None:
            self._config = config
        else:
            self._config: dict[str, any] = {"plot_title": "Traces",
                                            "y_label": "Power",
                                            "x_label": "Time",
                                            "data_title": [],
                                            "plot_size": (15, 10),
                                            "plot_output_name": "output.png",
                                            "plot_output_folder": AssignmentConfigManager.get_instance().output_folder_path+"\\",
                                            "plot_to_display": False,
                                            "plot_to_disk": True,
                                            "plot_line_colors": ['tab:blue', 'tab:orange', 'tab:green', 'tab:purple',
                                                                 'tab:red'],
                                            "plot_line_labels": None,
                                            "plot_enable_legend": False,
                                            "plot_annotation_at": None
                                            }
        self.data = data

    @property
    def config(self) -> dict[str, any]:
        """
        Property to get the current configuration settings.

        Returns:
            dict: The current configuration settings.
        """
        return self._config

    def data_to_plot(self) -> None:
        """
        Manages the entire plotting process based on the configuration settings.

        It sets up the plot, processes the data, adds a legend (if enabled), and either displays
        the plot on the screen or saves it to a file based on the configuration settings.
        """
        self.plot_setup()
        self.plot_data_processing()
        if self.config.get("plot_enable_legend", False):
            plot.legend()

        if self._config.get("plot_to_display", False):
            self.plot_to_display()
        elif self._config.get("plot_to_disk", False):
            self.plot_to_file()
        else:
            print("No output option selected. Set 'plot_to_display' or 'plot_to_disk' to True in the configuration.")

    def plot_setup(self) -> None:
        """
        Sets up the main figure and its title.
        """
        if self._config.get("plot_size", None) is not None:
            self.figure = plot.figure(figsize=self._config.get("plot_size", ()))
        else:
            self.figure = plot.figure()

        self.figure.suptitle(self._config.get("plot_title", "NOT SET"))

    def plot_data_processing(self) -> None:
        """
        Handles the data plotting and line styling.

        It creates a subplot for each trace in the data, sets the line color, label, and the axis labels.
        """
        ax = self.figure.add_subplot(1, 1, 1)
        for i, trace in enumerate(self.data, start=0):
            if self.config.get("plot_line_labels", None) is not None:
                label = self.config.get("plot_line_labels", "")[i]
                ax.plot(trace, color=self._config.get("plot_line_colors")[i], label=label)
            else:
                ax.plot(trace, color=self._config.get("plot_line_colors")[i])
            plot.xlabel(self._config.get("x_label"))
            plot.ylabel(self._config.get("y_label"))
            self.add_annotations(ax, i)

    def add_annotations(self, ax, trace) -> None:
        if self._config.get("plot_annotation_at", None) is not None:
            entry = self._config.get("plot_annotation_at", [])[trace]
            coords = entry[0]
            text = entry[1]
            ax.annotate(text, # this is the text
                 coords, # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

    def plot_to_file(self) -> None:
        """
        Saves the current plot to a file.

        The file path is constructed from the 'plot_output_folder' and 'plot_output_name' configuration settings.
        """
        filepath: str = self._config.get("plot_output_folder") + self._config.get("plot_output_name")
        plot.savefig(filepath)

    def plot_to_display(self) -> None:
        """
        Displays the plot on the screen.
        """
        plot.show()

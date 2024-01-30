import tkinter as tk
from tkinter import messagebox
from starting.arguments import arguments

class Interface:
    """
    Represents the user interface for choosing algorithm options.

    Usage:
    - Initialize with __init__()

    Methods:
    - on_algorithm_change(*args): Callback for algorithm change event.
    - on_file_change(*args): Callback for 'Use previous run file' checkbox change event.
    - on_breath_change(*args): Callback for 'Breath-first' checkbox change event.
    - on_dijkstra_change(*args): Callback for 'Dijkstra' checkbox change event.
    - on_button_click(): Callback for 'Apply' button click event.
    - perform_animation_and_dismiss(): Placeholder function for animation logic.
    - create_widgets(): Creates Tkinter widgets and arranges them in the window.
    - run(): Enters the Tkinter main event loop to run the application.
    """

    def __init__(self):
        """
        Initializes the Choices object and creates the Tkinter window.
        """
        self.root: tk.Tk = tk.Tk()
        self.root.title("Choose algorithms")

        self.out = []

        self.algorithm: tk.StringVar = tk.StringVar(value="random")
        self.filename: tk.StringVar = tk.StringVar(value="")
        self.n: tk.StringVar = tk.StringVar(value="1")
        self.switches: tk.BooleanVar = tk.BooleanVar(value=False)
        self.breath: tk.BooleanVar = tk.BooleanVar(value=False)
        self.m: tk.StringVar = tk.StringVar(value="1")
        self.dijkstra: tk.BooleanVar = tk.BooleanVar(value=False)
        self.hist: tk.BooleanVar = tk.BooleanVar(value=False)
        self.csv: tk.BooleanVar = tk.BooleanVar(value=False)
        self.visualize: tk.BooleanVar = tk.BooleanVar(value=False)
        self.output: tk.StringVar = tk.StringVar(value="")
        self.district: tk.StringVar = tk.StringVar(value="1")

        self.previous: tk.BooleanVar = tk.BooleanVar(value=True)

        self.create_widgets()

    def reset_variables(self):
        """
        Resets the variables to their initial values.
        """
        self.filename.set("")
        self.n.set("1")
        self.switches.set(False)
        self.breath.set(False)
        self.m.set("1")
        self.dijkstra.set(False)
        self.hist.set(False)
        self.csv.set(False)
        self.visualize.set(False)
        self.output.set("")
        self.district.set("1")
        self.previous.set(True)

    def validate_numeric_input(self, action, value_if_allowed, current_value, new_input, validation_type, trigger_type, widget_name):
        """
        Validation function to allow only numeric input (excluding leading 0) or an empty string.
        """
        if action == '1':  # insert
            if new_input.isdigit() or (new_input == "" and current_value != ""):
                # Allow only numeric input or an empty string, excluding leading 0
                return not (new_input == "0" and current_value == "")
            else:
                return False
        else:
            return True



    def on_algorithm_change(self, *args):
        """
        Callback for the algorithm change event.
        Adjusts the visibility of certain widgets based on the selected algorithm.
        """
        # Reset variables when the algorithm changes
        self.reset_variables()

        current_algorithm: str = self.algorithm.get()

        self.iterations_label.grid_remove()
        self.iterations_entry.grid_remove()
        self.previous_file_checkbox.grid_remove()
        self.filename_label.grid_remove()
        self.filename_entry.grid_remove()
        self.hist_checkbox.grid_remove()
        self.csv_checkbox.grid_remove()

        if current_algorithm == "random":
            self.iterations_label.grid(row=1, column=0, sticky="e", pady=5)
            self.iterations_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)
            self.hist_checkbox.grid(row=7, column=1, sticky="w", pady=5)
            self.csv_checkbox.grid(row=7, column=2, sticky="w", pady=5)

        elif current_algorithm == "file":
            self.previous_file_checkbox.grid(row=1, column=1, sticky="w", pady=5)

    def on_file_change(self, *args):
        """
        Callback for the 'Use previous run file' checkbox change event.
        Adjusts the visibility of the filename-related widgets based on the checkbox state.
        """
        if not self.previous.get():
            self.filename_label.grid(row=2, column=0, sticky="e", pady=5)
            self.filename_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        else:
            self.filename_label.grid_remove()
            self.filename_entry.grid_remove()

    def on_breath_change(self, *args):
        """
        Callback for the 'Breath-first' checkbox change event.
        Adjusts the visibility of the 'Main Branches' widgets based on the checkbox state.
        """
        if self.breath.get():
            self.dijkstra.set(False)
            self.main_branches_label.grid(row=6, column=0, sticky="e", pady=5)
            self.main_branches_menu.grid(row=6, column=1, columnspan=2, sticky="w", pady=5)
        else:
            self.main_branches_label.grid_remove()
            self.main_branches_menu.grid_remove()

    def on_dijkstra_change(self, *args):
        """
        Callback for the 'Dijkstra' checkbox change event.
        Adjusts the visibility of the 'Main Branches' widgets based on the checkbox state.
        """
        if self.dijkstra.get():
            self.main_branches_label.grid_remove()
            self.main_branches_menu.grid_remove()
            self.breath.set(False)

    def on_button_click(self):
        """
        Callback for the 'Apply' button click event.
        """



        # Schedule the animation and window dismissal after 2 seconds
        self.root.after(200, self.perform_animation_and_dismiss)

        # Return a list containing the arguments used
        out = []
        if self.algorithm.get() == "random":
            out.append("-r")
            out.append("-n")
            out.append(self.n.get())

        elif self.algorithm.get() == "greedy":
            out.append("-g")
        elif self.algorithm.get() == "file":
            out.append("-f")
            if self.filename.get():
                out.append("-i")
                out.append(self.filename.get())
        
        if self.switches.get():
            out.append("-s")


        if self.dijkstra.get():
            out.append("-d")


        elif self.breath.get():
            out.append("-b")
            out.append("-m")
            out.append(self.m.get())

        if self.visualize.get():
            out.append("-v")

        if self.hist.get():
            out.append("-p")

        if self.csv.get():
            out.append("-c")

        if self.output.get():
            out.append("-o")
            out.append(self.output.get())

        out.append(self.district.get())


        self.out = out

    def perform_animation_and_dismiss(self):
        """
        Placeholder function for animation logic.
        Displays a messagebox and dismisses the Tkinter window.
        """
        self.root.destroy()

    def create_widgets(self):
        """
        Creates Tkinter widgets and arranges them in the window.
        """
        self.algorithm_label: tk.Label = tk.Label(self.root, text="Start algorithm:")
        self.algorithm_options: list[str] = ["random", "greedy", "file"]
        self.algorithm_entry: tk.OptionMenu = tk.OptionMenu(self.root, self.algorithm, *self.algorithm_options,
                                                            command=self.on_algorithm_change)

        self.iterations_label: tk.Label = tk.Label(self.root, text="Iterations:")
        self.iterations_entry: tk.Entry = tk.Entry(self.root, textvariable=self.n)

        self.previous_file_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Use previous run file",
                                                                      variable=self.previous, command=self.on_file_change)

        self.filename_label: tk.Label = tk.Label(self.root, text="Input filename:")
        self.filename_entry: tk.Entry = tk.Entry(self.root, textvariable=self.filename)

        self.switches_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Switches", variable=self.switches)
        self.breath_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Breath-first greedy", variable=self.breath,
                                                              command=self.on_breath_change)

        self.main_branches_label: tk.Label = tk.Label(self.root, text="Main Branches:")
        self.main_branches_options: list[str] = ["1", "2", "3", "4", "5"]
        self.main_branches_menu: tk.OptionMenu = tk.OptionMenu(self.root, self.m, *self.main_branches_options)

        self.dijkstra_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Dijkstra", variable=self.dijkstra,
                                                                command=self.on_dijkstra_change)

        self.output_label: tk.Label = tk.Label(self.root, text="Save output as:")
        self.output_entry: tk.Entry = tk.Entry(self.root, textvariable=self.output)

        self.visualize_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Visualize grid result",
                                                                 variable=self.visualize)
        self.hist_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="Show histogram", variable=self.hist)
        self.csv_checkbox: tk.Checkbutton = tk.Checkbutton(self.root, text="CSV", variable=self.csv)

        # GUI PLACEMENT
        self.district_label: tk.Label = tk.Label(self.root, text="District:")
        self.district_var_options: list[str] = ["1", "2", "3"]
        self.district_var_menu: tk.OptionMenu = tk.OptionMenu(self.root, self.district, *self.district_var_options)

        self.apply_button: tk.Button = tk.Button(self.root, text="Apply", command=self.on_button_click)

        self.algorithm_label.grid(row=0, column=0, sticky="e", pady=5)
        self.algorithm_entry.grid(row=0, column=1, columnspan=2, sticky="w", pady=5)

        self.iterations_label.grid(row=1, column=0, sticky="e", pady=5)
        self.iterations_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)
        self.iterations_entry.config(validate="key", validatecommand=(self.root.register(self.validate_numeric_input), '%d', '%P', '%s', '%S', '%v', '%V', '%W'))
        self.hist_checkbox.grid(row=7, column=1, sticky="w", pady=5)
        self.csv_checkbox.grid(row=7, column=2, sticky="w", pady=5)

        self.switches_checkbox.grid(row=3, column=1, sticky="w", pady=5)
        self.breath_checkbox.grid(row=4, column=1, sticky="w", pady=5)
        self.dijkstra_checkbox.grid(row=4, column=2, sticky="w", pady=5)

        self.visualize_checkbox.grid(row=8, column=1, sticky="w", pady=5)

        self.district_label.grid(row=0, column=1, sticky="e", pady=5)
        self.district_var_menu.grid(row=0, column=2, columnspan=2, sticky="w", pady=5)

        self.output_label.grid(row=10, column=0, sticky="e", pady=5)
        self.output_entry.grid(row=10, column=1, columnspan=2, sticky="w", pady=5)

        self.apply_button.grid(row=11, column=1, columnspan=2, pady=10)

    def run(self):
        """
        Enters the Tkinter main event loop to run the application.
        """
        self.root.mainloop()

        if not self.out:
            return False
        return arguments(self.out)

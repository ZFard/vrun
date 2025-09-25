#!/usr/bin/env python3
"""
VASP DOS Plotter GUI Application
An intuitive interface for plotting and analyzing VASP DOS data
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import threading
import queue
import time
from PIL import Image, ImageTk

class DOSPlotterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VASP DOS Plotter - Professional Edition")
        self.root.geometry("1200x680")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.energies = None
        self.dos_values = None
        self.current_file = None
        
        # Threading and responsiveness
        self.plot_queue = queue.Queue()
        self.is_plotting = False
        self.last_update_time = 0
        self.update_delay = 0.3  # Delay between updates in seconds
        
        # Plotting mode tracking
        self.plotting_mode = "single"  # "single" or "multi"
        self.multi_file_data = []  # Store multi-file data for context-aware updates
        
        # Default settings
        self.settings = {
            'energy_min': -7.0,
            'energy_max': 7.0,
            'line_width': 2,
            'line_color': 'blue',
            'fermi_color': 'red',
            'grid_alpha': 0.3,
            'figure_width': 12,
            'figure_height': 8,
            'dpi': 300,
            'font_size': 12,
            'title_font_size': 16,
            'show_fermi': True,
            'show_grid': True,
            'auto_scale': True
        }
        
        self.setup_ui()
        self.setup_auto_update()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frames
        self.create_menu_bar()
        self.create_main_frames()
        self.create_file_frame()
        self.create_settings_frame()
        self.create_plot_frame()
        self.create_status_frame()
        
    def setup_auto_update(self):
        """Setup automatic plot updates"""
        self.root.after(100, self.check_plot_queue)
        
    def check_plot_queue(self):
        """Check for pending plot updates"""
        try:
            while True:
                self.plot_queue.get_nowait()
                self.update_plot_safe()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_plot_queue)
            
    def schedule_plot_update(self):
        """Schedule a plot update with debouncing"""
        current_time = time.time()
        if current_time - self.last_update_time > self.update_delay:
            self.last_update_time = current_time
            self.plot_queue.put("update")
            
    def validate_and_update(self):
        """Validate energy range inputs and update plot"""
        try:
            # Try to get the values to validate them
            min_val = float(self.energy_min_var.get())
            max_val = float(self.energy_max_var.get())
            
            # Basic validation
            if min_val >= max_val:
                self.progress_var.set("Min must be < Max")
                return
                
            if abs(min_val) > 1000 or abs(max_val) > 1000:
                self.progress_var.set("Values too large")
                return
                
            # If validation passes, schedule update
            self.schedule_plot_update()
            
        except (ValueError, tk.TclError):
            # Invalid input, don't update plot
            self.progress_var.set("Invalid input")
            return
            
    def slider_update(self, slider_type):
        """Handle slider updates with immediate feedback"""
        try:
            min_val = float(self.energy_min_var.get())
            max_val = float(self.energy_max_var.get())
            
            # Update slider info with mode context
            mode_text = "Multi-file" if self.plotting_mode == "multi" else "Single file"
            self.slider_info_var.set(f"{mode_text} Range: {min_val:.2f} to {max_val:.2f} eV")
            
            # Ensure min < max
            if min_val >= max_val:
                if slider_type == 'min':
                    self.energy_max_var.set(min_val + 0.1)
                else:
                    self.energy_min_var.set(max_val - 0.1)
                return
            
            # Update plot immediately for smooth interaction
            self.schedule_plot_update()
            
        except (ValueError, tk.TclError):
            pass
        
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open DOS File", command=self.open_file)
        file_menu.add_command(label="Save Plot", command=self.save_plot)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Reset to Defaults", command=self.reset_settings)
        settings_menu.add_command(label="Load Settings", command=self.load_settings)
        settings_menu.add_command(label="Save Settings", command=self.save_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_help)
        
    def create_main_frames(self):
        """Create main layout frames"""
        # Top frame for file and settings
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill='x', padx=10, pady=5)
        
        # Bottom frame for plot
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
    def create_file_frame(self):
        """Create file selection frame with tabs"""
        file_frame = ttk.LabelFrame(self.top_frame, text="File Operations", padding=5)
        file_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Create notebook for file operations
        file_notebook = ttk.Notebook(file_frame)
        file_notebook.pack(fill='both', expand=True)
        
        # Single file tab
        self.create_single_file_tab(file_notebook)
        
        # Bulk operations tab
        self.create_bulk_operations_tab(file_notebook)
        
    def create_single_file_tab(self, notebook):
        """Create single file operations tab"""
        single_frame = ttk.Frame(notebook)
        notebook.add(single_frame, text="Single File")
        
        # File selection
        ttk.Label(single_frame, text="DOS File:").pack(anchor='w')
        file_select_frame = ttk.Frame(single_frame)
        file_select_frame.pack(fill='x', pady=(0, 5))
        
        self.file_var = tk.StringVar(value="No file selected")
        self.file_label = ttk.Label(file_select_frame, textvariable=self.file_var, 
                                   background='white', relief='sunken', anchor='w')
        self.file_label.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ttk.Button(file_select_frame, text="Browse", 
                  command=self.open_file).pack(side='right')
        
        # Quick load buttons
        quick_frame = ttk.Frame(single_frame)
        quick_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Button(quick_frame, text="Load RES/DOS0", 
                  command=lambda: self.load_file("RES/DOS0")).pack(side='left', padx=(0, 3))
        ttk.Button(quick_frame, text="Load Sample", 
                  command=self.load_sample_data).pack(side='left', padx=(0, 3))
        ttk.Button(quick_frame, text="About", 
                  command=self.show_about).pack(side='left')
        
        # File info
        self.file_info = scrolledtext.ScrolledText(single_frame, height=3, width=40)
        self.file_info.pack(fill='x', pady=(5, 0))
        
    def create_bulk_operations_tab(self, notebook):
        """Create multi-file plotting tab"""
        bulk_frame = ttk.Frame(notebook)
        notebook.add(bulk_frame, text="Multi-File Plot")
        
        # File selection for multi-file plotting
        ttk.Label(bulk_frame, text="Select Files to Plot Together:").pack(anchor='w')
        
        # File list with scrollbar
        list_frame = ttk.Frame(bulk_frame)
        list_frame.pack(fill='x', pady=(0, 5))
        
        self.bulk_files_listbox = tk.Listbox(list_frame, height=4, selectmode=tk.MULTIPLE)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.bulk_files_listbox.yview)
        self.bulk_files_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.bulk_files_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # File selection buttons
        file_buttons_frame = ttk.Frame(bulk_frame)
        file_buttons_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Button(file_buttons_frame, text="Add Files", 
                  command=self.add_bulk_files).pack(side='left', padx=(0, 3))
        ttk.Button(file_buttons_frame, text="Clear List", 
                  command=self.clear_bulk_files).pack(side='left', padx=(0, 3))
        ttk.Button(file_buttons_frame, text="Remove Selected", 
                  command=self.remove_selected_bulk_files).pack(side='left')
        
        # Color settings
        color_frame = ttk.Frame(bulk_frame)
        color_frame.pack(fill='x', pady=(5, 5))
        
        ttk.Label(color_frame, text="Color Scheme:").pack(side='left')
        self.color_scheme_var = tk.StringVar(value="auto")
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_scheme_var,
                                  values=['auto', 'rainbow', 'viridis', 'plasma', 'tab10'], width=10)
        color_combo.pack(side='left', padx=(5, 0))
        
        # Multi-file operation buttons
        bulk_buttons_frame = ttk.Frame(bulk_frame)
        bulk_buttons_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Button(bulk_buttons_frame, text="Plot All Together", 
                  command=self.plot_all_files_together).pack(side='left', padx=(0, 3))
        ttk.Button(bulk_buttons_frame, text="Clear Plot", 
                  command=self.clear_multi_plot).pack(side='left', padx=(0, 3))
        ttk.Button(bulk_buttons_frame, text="Save Multi-Plot", 
                  command=self.save_multi_plot).pack(side='left')
        
        # Progress indicator
        self.bulk_progress_var = tk.StringVar(value="Ready for multi-file plotting")
        ttk.Label(bulk_frame, textvariable=self.bulk_progress_var, 
                 font=('Arial', 8), foreground='blue').pack(anchor='w', pady=(5, 0))
        
    def create_settings_frame(self):
        """Create settings frame"""
        settings_frame = ttk.LabelFrame(self.top_frame, text="Plot Settings", padding=5)
        settings_frame.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Create notebook for organized settings
        notebook = ttk.Notebook(settings_frame)
        notebook.pack(fill='both', expand=True)
        
        # Energy range tab
        self.create_energy_tab(notebook)
        
        # Appearance tab
        self.create_appearance_tab(notebook)
        
        # Export tab
        self.create_export_tab(notebook)
        
    def create_energy_tab(self, notebook):
        """Create energy range settings tab"""
        energy_frame = ttk.Frame(notebook)
        notebook.add(energy_frame, text="Energy Range")
        
        # Energy range - compact layout
        ttk.Label(energy_frame, text="Energy Range (eV):").pack(anchor='w', pady=(0, 3))
        
        # Text entry fields - more compact
        range_frame = ttk.Frame(energy_frame)
        range_frame.pack(fill='x', pady=(0, 3))
        
        ttk.Label(range_frame, text="Min:").pack(side='left')
        self.energy_min_var = tk.DoubleVar(value=self.settings['energy_min'])
        self.energy_min_entry = ttk.Entry(range_frame, textvariable=self.energy_min_var, width=8)
        self.energy_min_entry.pack(side='left', padx=(3, 8))
        self.energy_min_var.trace('w', lambda *args: self.validate_and_update())
        
        ttk.Label(range_frame, text="Max:").pack(side='left')
        self.energy_max_var = tk.DoubleVar(value=self.settings['energy_max'])
        self.energy_max_entry = ttk.Entry(range_frame, textvariable=self.energy_max_var, width=8)
        self.energy_max_entry.pack(side='left', padx=(3, 0))
        self.energy_max_var.trace('w', lambda *args: self.validate_and_update())
        
        # Interactive sliders - more compact
        ttk.Label(energy_frame, text="Sliders:").pack(anchor='w', pady=(3, 0))
        
        # Min energy slider - compact
        min_slider_frame = ttk.Frame(energy_frame)
        min_slider_frame.pack(fill='x', pady=(1, 2))
        
        ttk.Label(min_slider_frame, text="Min:", width=6).pack(side='left')
        self.energy_min_slider = ttk.Scale(min_slider_frame, from_=-20, to=20, 
                                          variable=self.energy_min_var, orient='horizontal',
                                          command=lambda x: self.slider_update('min'))
        self.energy_min_slider.pack(side='left', fill='x', expand=True, padx=(3, 3))
        
        # Max energy slider - compact
        max_slider_frame = ttk.Frame(energy_frame)
        max_slider_frame.pack(fill='x', pady=(1, 2))
        
        ttk.Label(max_slider_frame, text="Max:", width=6).pack(side='left')
        self.energy_max_slider = ttk.Scale(max_slider_frame, from_=-20, to=20, 
                                          variable=self.energy_max_var, orient='horizontal',
                                          command=lambda x: self.slider_update('max'))
        self.energy_max_slider.pack(side='left', fill='x', expand=True, padx=(3, 3))
        
        # Slider info - smaller
        self.slider_info_var = tk.StringVar(value="Drag sliders to adjust range")
        ttk.Label(energy_frame, textvariable=self.slider_info_var, 
                 font=('Arial', 7), foreground='gray').pack(anchor='w', pady=(1, 0))
        
        # Control buttons - more compact
        button_frame = ttk.Frame(energy_frame)
        button_frame.pack(fill='x', pady=(3, 5))
        
        ttk.Button(button_frame, text="Auto-detect", 
                  command=self.auto_detect_range).pack(side='left', padx=(0, 3))
        ttk.Button(button_frame, text="Zoom Data", 
                  command=self.zoom_to_data_range).pack(side='left', padx=(0, 3))
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset_to_default_range).pack(side='left')
        
        # Fermi level - more compact
        fermi_frame = ttk.Frame(energy_frame)
        fermi_frame.pack(fill='x', pady=(0, 5))
        
        self.show_fermi_var = tk.BooleanVar(value=self.settings['show_fermi'])
        ttk.Checkbutton(fermi_frame, text="Fermi Level", 
                       variable=self.show_fermi_var,
                       command=self.schedule_plot_update).pack(side='left')
        
        ttk.Label(fermi_frame, text="Color:").pack(side='left', padx=(15, 3))
        self.fermi_color_var = tk.StringVar(value=self.settings['fermi_color'])
        fermi_color_combo = ttk.Combobox(fermi_frame, textvariable=self.fermi_color_var,
                                        values=['red', 'black', 'green', 'blue', 'orange'], width=8)
        fermi_color_combo.pack(side='left')
        self.fermi_color_var.trace('w', lambda *args: self.schedule_plot_update())
        
    def create_appearance_tab(self, notebook):
        """Create appearance settings tab"""
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        
        # Line settings - compact
        ttk.Label(appearance_frame, text="Line:").pack(anchor='w', pady=(0, 3))
        
        line_frame = ttk.Frame(appearance_frame)
        line_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(line_frame, text="Width:").pack(side='left')
        self.line_width_var = tk.DoubleVar(value=self.settings['line_width'])
        ttk.Scale(line_frame, from_=0.5, to=5.0, variable=self.line_width_var, 
                 orient='horizontal', length=80,
                 command=lambda x: self.schedule_plot_update()).pack(side='left', padx=(3, 8))
        
        ttk.Label(line_frame, text="Color:").pack(side='left')
        self.line_color_var = tk.StringVar(value=self.settings['line_color'])
        line_color_combo = ttk.Combobox(line_frame, textvariable=self.line_color_var,
                                       values=['blue', 'red', 'green', 'black', 'purple', 'orange'], width=8)
        line_color_combo.pack(side='left')
        self.line_color_var.trace('w', lambda *args: self.schedule_plot_update())
        
        # Grid settings - compact
        grid_frame = ttk.Frame(appearance_frame)
        grid_frame.pack(fill='x', pady=(0, 5))
        
        self.show_grid_var = tk.BooleanVar(value=self.settings['show_grid'])
        ttk.Checkbutton(grid_frame, text="Grid", 
                       variable=self.show_grid_var,
                       command=self.schedule_plot_update).pack(side='left')
        
        ttk.Label(grid_frame, text="Alpha:").pack(side='left', padx=(15, 3))
        self.grid_alpha_var = tk.DoubleVar(value=self.settings['grid_alpha'])
        ttk.Scale(grid_frame, from_=0.1, to=1.0, variable=self.grid_alpha_var, 
                 orient='horizontal', length=80,
                 command=lambda x: self.schedule_plot_update()).pack(side='left')
        
        # Font settings - compact
        ttk.Label(appearance_frame, text="Font:").pack(anchor='w', pady=(5, 3))
        
        font_frame = ttk.Frame(appearance_frame)
        font_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(font_frame, text="Size:").pack(side='left')
        self.font_size_var = tk.IntVar(value=self.settings['font_size'])
        ttk.Scale(font_frame, from_=8, to=20, variable=self.font_size_var, 
                 orient='horizontal', length=80,
                 command=lambda x: self.schedule_plot_update()).pack(side='left', padx=(3, 8))
        
        ttk.Label(font_frame, text="Title:").pack(side='left')
        self.title_font_size_var = tk.IntVar(value=self.settings['title_font_size'])
        ttk.Scale(font_frame, from_=12, to=24, variable=self.title_font_size_var, 
                 orient='horizontal', length=80,
                 command=lambda x: self.schedule_plot_update()).pack(side='left', padx=(3, 0))
        
    def create_export_tab(self, notebook):
        """Create export settings tab"""
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="Export")
        
        # Figure size - compact
        ttk.Label(export_frame, text="Size:").pack(anchor='w', pady=(0, 3))
        
        size_frame = ttk.Frame(export_frame)
        size_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(size_frame, text="W:").pack(side='left')
        self.figure_width_var = tk.DoubleVar(value=self.settings['figure_width'])
        ttk.Entry(size_frame, textvariable=self.figure_width_var, width=6).pack(side='left', padx=(3, 8))
        
        ttk.Label(size_frame, text="H:").pack(side='left')
        self.figure_height_var = tk.DoubleVar(value=self.settings['figure_height'])
        ttk.Entry(size_frame, textvariable=self.figure_height_var, width=6).pack(side='left', padx=(3, 0))
        
        # DPI - compact
        ttk.Label(export_frame, text="DPI:").pack(anchor='w', pady=(5, 3))
        self.dpi_var = tk.IntVar(value=self.settings['dpi'])
        ttk.Scale(export_frame, from_=100, to=600, variable=self.dpi_var, 
                 orient='horizontal', length=150).pack(fill='x', pady=(0, 5))
        
        # Export buttons - compact
        ttk.Button(export_frame, text="Save PNG", 
                  command=self.save_plot).pack(fill='x', pady=(0, 3))
        ttk.Button(export_frame, text="Export CSV", 
                  command=self.export_data).pack(fill='x', pady=(0, 3))
        ttk.Button(export_frame, text="Copy", 
                  command=self.copy_plot).pack(fill='x')
        
    def create_plot_frame(self):
        """Create plot display frame"""
        plot_frame = ttk.LabelFrame(self.bottom_frame, text="DOS Plot", padding=10)
        plot_frame.pack(fill='both', expand=True)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Plot controls
        controls_frame = ttk.Frame(plot_frame)
        controls_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(controls_frame, text="Update Plot", 
                  command=self.update_plot).pack(side='left', padx=(0, 10))
        ttk.Button(controls_frame, text="Reset View", 
                  command=self.reset_view).pack(side='left', padx=(0, 10))
        ttk.Button(controls_frame, text="Zoom to Data", 
                  command=self.zoom_to_data).pack(side='left', padx=(0, 10))
        
        # Add progress indicator
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(controls_frame, textvariable=self.progress_var, 
                 foreground='blue').pack(side='right')
        
    def create_status_frame(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill='x', side='bottom')
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.status_frame, textvariable=self.status_var, 
                 relief='sunken', anchor='w').pack(fill='x')
        
    def open_file(self):
        """Open file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select DOS File",
            filetypes=[("DOS files (no extension)", "*."), ("All files", "*.*"), ("Text files", "*.txt")]
        )
        if file_path:
            self.load_file(file_path)
            
    def load_file(self, file_path):
        """Load DOS file with threading"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
            
        # Start loading in a separate thread
        self.progress_var.set("Loading file...")
        self.status_var.set("Loading file...")
        
        def load_thread():
            try:
                energies, dos_values = self.read_dos_file(file_path)
                
                if len(energies) == 0:
                    self.root.after(0, lambda: messagebox.showerror("Error", "No valid data found in file"))
                    return
                    
                # Update data in main thread
                self.root.after(0, lambda: self.finish_file_loading(energies, dos_values, file_path))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_load_error(str(e)))
        
        threading.Thread(target=load_thread, daemon=True).start()
        
    def finish_file_loading(self, energies, dos_values, file_path):
        """Finish file loading in main thread"""
        try:
            self.energies = energies
            self.dos_values = dos_values
            self.current_file = file_path
            
            # Set plotting mode to single file
            self.plotting_mode = "single"
            self.multi_file_data = []
            
            # Update UI
            self.file_var.set(os.path.basename(file_path))
            self.update_file_info()
            self.auto_detect_range()
            self.update_plot()
            
            self.status_var.set(f"Loaded {len(energies)} data points")
            self.progress_var.set("Ready")
            
        except Exception as e:
            self.handle_load_error(str(e))
            
    def handle_load_error(self, error_msg):
        """Handle file loading errors"""
        messagebox.showerror("Error", f"Failed to load file: {error_msg}")
        self.status_var.set("Error loading file")
        self.progress_var.set("Error")
            
    def read_dos_file(self, filename):
        """Read DOS data from file"""
        energies = []
        dos_values = []
        
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        energy = float(parts[0])
                        dos_value = float(parts[1])
                        energies.append(energy)
                        dos_values.append(dos_value)
                    except ValueError:
                        continue
        
        return np.array(energies), np.array(dos_values)
        
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Generate sample data
        energies = np.linspace(-10, 10, 200)
        dos = (np.exp(-(energies + 5)**2 / 2) + 
               0.8 * np.exp(-(energies + 2)**2 / 1.5) +
               0.6 * np.exp(-(energies - 1)**2 / 1) +
               0.4 * np.exp(-(energies - 4)**2 / 2))
        
        self.energies = energies
        self.dos_values = dos
        self.current_file = "Sample Data"
        
        self.file_var.set("Sample Data")
        self.update_file_info()
        self.auto_detect_range()
        self.update_plot()
        
        self.status_var.set("Loaded sample data")
        
    def update_file_info(self):
        """Update file information display"""
        if self.energies is None:
            return
            
        info = f"Data Points: {len(self.energies)}\n"
        info += f"Energy Range: {self.energies.min():.3f} to {self.energies.max():.3f} eV\n"
        info += f"DOS Range: {self.dos_values.min():.3f} to {self.dos_values.max():.3f} states/eV\n"
        info += f"Average DOS: {self.dos_values.mean():.3f} states/eV"
        
        self.file_info.delete(1.0, tk.END)
        self.file_info.insert(1.0, info)
        
    def auto_detect_range(self):
        """Auto-detect reasonable energy range based on current mode"""
        if self.plotting_mode == "multi" and self.multi_file_data:
            # Auto-detect range for multi-file data
            all_energies = []
            for energies, _, _ in self.multi_file_data:
                all_energies.extend(energies)
            
            if not all_energies:
                return
                
            all_energies = np.array(all_energies)
            
            # Find range that contains 95% of all data
            energy_min = np.percentile(all_energies, 2.5)
            energy_max = np.percentile(all_energies, 97.5)
            
            # Update the variables
            self.energy_min_var.set(energy_min)
            self.energy_max_var.set(energy_max)
            
            # Update slider ranges to accommodate all data
            data_min = all_energies.min()
            data_max = all_energies.max()
            
            # Set slider ranges with some padding
            slider_min = min(data_min - 2, energy_min - 1)
            slider_max = max(data_max + 2, energy_max + 1)
            
            self.energy_min_slider.configure(from_=slider_min, to=slider_max)
            self.energy_max_slider.configure(from_=slider_min, to=slider_max)
            
            # Update slider info
            self.slider_info_var.set(f"Multi-file auto-detected: {energy_min:.2f} to {energy_max:.2f} eV")
            
        elif self.plotting_mode == "single" and self.energies is not None:
            # Auto-detect range for single file data
            # Find range that contains 95% of the data
            energy_min = np.percentile(self.energies, 2.5)
            energy_max = np.percentile(self.energies, 97.5)
            
            # Update the variables
            self.energy_min_var.set(energy_min)
            self.energy_max_var.set(energy_max)
            
            # Update slider ranges to accommodate the data
            data_min = self.energies.min()
            data_max = self.energies.max()
            
            # Set slider ranges with some padding
            slider_min = min(data_min - 2, energy_min - 1)
            slider_max = max(data_max + 2, energy_max + 1)
            
            self.energy_min_slider.configure(from_=slider_min, to=slider_max)
            self.energy_max_slider.configure(from_=slider_min, to=slider_max)
            
            # Update slider info
            self.slider_info_var.set(f"Single file auto-detected: {energy_min:.2f} to {energy_max:.2f} eV")
        else:
            return
        
        # Update plot
        self.schedule_plot_update()
        
    def zoom_to_data_range(self):
        """Zoom to show all data with sliders based on current mode"""
        if self.plotting_mode == "multi" and self.multi_file_data:
            # Zoom to full range of all multi-file data
            all_energies = []
            for energies, _, _ in self.multi_file_data:
                all_energies.extend(energies)
            
            if not all_energies:
                return
                
            all_energies = np.array(all_energies)
            data_min = all_energies.min()
            data_max = all_energies.max()
            
            self.energy_min_var.set(data_min)
            self.energy_max_var.set(data_max)
            
            # Update slider ranges
            self.energy_min_slider.configure(from_=data_min - 1, to=data_max + 1)
            self.energy_max_slider.configure(from_=data_min - 1, to=data_max + 1)
            
            # Update slider info
            self.slider_info_var.set(f"Multi-file full range: {data_min:.2f} to {data_max:.2f} eV")
            
        elif self.plotting_mode == "single" and self.energies is not None:
            # Zoom to full range of single file data
            data_min = self.energies.min()
            data_max = self.energies.max()
            
            self.energy_min_var.set(data_min)
            self.energy_max_var.set(data_max)
            
            # Update slider ranges
            self.energy_min_slider.configure(from_=data_min - 1, to=data_max + 1)
            self.energy_max_slider.configure(from_=data_min - 1, to=data_max + 1)
            
            # Update slider info
            self.slider_info_var.set(f"Single file full range: {data_min:.2f} to {data_max:.2f} eV")
        else:
            return
        
        # Update plot
        self.schedule_plot_update()
        
    def reset_to_default_range(self):
        """Reset to default -7 to 7 eV range"""
        self.energy_min_var.set(-7.0)
        self.energy_max_var.set(7.0)
        
        # Update slider ranges
        self.energy_min_slider.configure(from_=-20, to=20)
        self.energy_max_slider.configure(from_=-20, to=20)
        
        # Update slider info
        self.slider_info_var.set("Default range: -7.00 to 7.00 eV")
        
        # Update plot
        self.schedule_plot_update()
        
    def update_plot_safe(self):
        """Safe plot update with error handling"""
        if self.is_plotting:
            return
            
        self.is_plotting = True
        try:
            self.update_plot()
        except Exception as e:
            self.progress_var.set(f"Error: {str(e)}")
            self.status_var.set(f"Plot error: {str(e)}")
        finally:
            self.is_plotting = False
            
    def update_plot(self):
        """Update the plot based on current mode"""
        if self.plotting_mode == "multi" and self.multi_file_data:
            self.update_multi_file_plot()
        elif self.plotting_mode == "single" and self.energies is not None:
            self.update_single_file_plot()
        else:
            self.progress_var.set("No data loaded")
            return
            
    def update_single_file_plot(self):
        """Update single file plot"""
        try:
            self.progress_var.set("Updating single file plot...")
            self.root.update_idletasks()
            
            self.ax.clear()
            
            # Get current settings with validation
            try:
                energy_min = float(self.energy_min_var.get())
                energy_max = float(self.energy_max_var.get())
            except (ValueError, tk.TclError):
                self.progress_var.set("Invalid energy range")
                return
                
            if energy_min >= energy_max:
                self.progress_var.set("Min energy must be less than max")
                return
            
            # Filter data
            mask = (self.energies >= energy_min) & (self.energies <= energy_max)
            filtered_energies = self.energies[mask]
            filtered_dos = self.dos_values[mask]
            
            if len(filtered_energies) == 0:
                self.ax.text(0.5, 0.5, 'No data in selected range', 
                           transform=self.ax.transAxes, ha='center', va='center')
                self.canvas.draw()
                self.progress_var.set("No data in range")
                return
            
            # Plot data
            self.ax.plot(filtered_energies, filtered_dos, 
                        color=self.line_color_var.get(),
                        linewidth=self.line_width_var.get(),
                        label='Total DOS')
            
            # Add Fermi level
            if self.show_fermi_var.get():
                self.ax.axvline(x=0, color=self.fermi_color_var.get(), 
                               linestyle='--', alpha=0.7, linewidth=2, 
                               label='Fermi Level')
            
            # Customize plot
            self.ax.set_xlabel('Energy (eV)', fontsize=self.font_size_var.get())
            self.ax.set_ylabel('Density of States (states/eV)', fontsize=self.font_size_var.get())
            self.ax.set_title('VASP Density of States', fontsize=self.title_font_size_var.get(), fontweight='bold')
            
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=self.grid_alpha_var.get())
            
            self.ax.legend()
            self.ax.set_xlim(energy_min, energy_max)
            
            # Auto-scale y-axis
            if self.settings.get('auto_scale', True):
                y_margin = (filtered_dos.max() - filtered_dos.min()) * 0.05
                self.ax.set_ylim(filtered_dos.min() - y_margin, filtered_dos.max() + y_margin)
            
            self.canvas.draw()
            
            # Update status
            self.status_var.set(f"Single file plot updated: {len(filtered_energies)} points in range")
            self.progress_var.set("Ready")
            
        except Exception as e:
            self.progress_var.set(f"Error: {str(e)}")
            self.status_var.set(f"Plot error: {str(e)}")
            raise
            
    def update_multi_file_plot(self):
        """Update multi-file plot"""
        try:
            self.progress_var.set("Updating multi-file plot...")
            self.root.update_idletasks()
            
            self.ax.clear()
            
            # Get current settings with validation
            try:
                energy_min = float(self.energy_min_var.get())
                energy_max = float(self.energy_max_var.get())
            except (ValueError, tk.TclError):
                self.progress_var.set("Invalid energy range")
                return
                
            if energy_min >= energy_max:
                self.progress_var.set("Min energy must be less than max")
                return
            
            # Generate colors based on scheme
            colors = self.generate_colors(len(self.multi_file_data))
            
            # Plot each file with different color
            all_dos_values = []
            for i, (energies, dos_values, file_path) in enumerate(self.multi_file_data):
                # Filter data
                mask = (energies >= energy_min) & (energies <= energy_max)
                filtered_energies = energies[mask]
                filtered_dos = dos_values[mask]
                
                if len(filtered_energies) > 0:
                    # Format legend label with path information
                    legend_label = self.format_legend_label(file_path)
                    
                    # Plot with unique color and formatted path as label
                    self.ax.plot(filtered_energies, filtered_dos, 
                               color=colors[i],
                               linewidth=self.line_width_var.get(),
                               label=legend_label)
                    all_dos_values.extend(filtered_dos)
            
            if not all_dos_values:
                self.ax.text(0.5, 0.5, 'No data in selected range', 
                           transform=self.ax.transAxes, ha='center', va='center')
                self.canvas.draw()
                self.progress_var.set("No data in range")
                return
            
            # Add Fermi level if enabled
            if self.show_fermi_var.get():
                self.ax.axvline(x=0, color=self.fermi_color_var.get(), 
                               linestyle='--', alpha=0.7, linewidth=2, 
                               label='Fermi Level')
            
            # Customize plot
            self.ax.set_xlabel('Energy (eV)', fontsize=self.font_size_var.get())
            self.ax.set_ylabel('Density of States (states/eV)', fontsize=self.font_size_var.get())
            self.ax.set_title('Multi-File DOS Comparison', fontsize=self.title_font_size_var.get(), fontweight='bold')
            
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=self.grid_alpha_var.get())
            
            # Add legend
            self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            self.ax.set_xlim(energy_min, energy_max)
            
            # Auto-scale y-axis based on all data
            if self.settings.get('auto_scale', True):
                y_margin = (max(all_dos_values) - min(all_dos_values)) * 0.05
                self.ax.set_ylim(min(all_dos_values) - y_margin, max(all_dos_values) + y_margin)
            
            self.canvas.draw()
            
            # Update status
            self.status_var.set(f"Multi-file plot updated: {len(self.multi_file_data)} files, {len(all_dos_values)} points in range")
            self.progress_var.set("Ready")
            
        except Exception as e:
            self.progress_var.set(f"Error: {str(e)}")
            self.status_var.set(f"Multi-file plot error: {str(e)}")
            raise
            
    def reset_view(self):
        """Reset plot view"""
        if self.energies is None:
            return
        self.auto_detect_range()
        self.update_plot()
        
    def zoom_to_data(self):
        """Zoom to show all data"""
        if self.energies is None:
            return
        self.energy_min_var.set(self.energies.min())
        self.energy_max_var.set(self.energies.max())
        self.update_plot()
        
    def save_plot(self):
        """Save plot to file"""
        if self.energies is None:
            messagebox.showwarning("Warning", "No data to plot")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Plot",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if file_path:
            try:
                # Create new figure with export settings
                fig = Figure(figsize=(self.figure_width_var.get(), self.figure_height_var.get()), 
                           dpi=self.dpi_var.get())
                ax = fig.add_subplot(111)
                
                # Recreate plot
                energy_min = self.energy_min_var.get()
                energy_max = self.energy_max_var.get()
                mask = (self.energies >= energy_min) & (self.energies <= energy_max)
                filtered_energies = self.energies[mask]
                filtered_dos = self.dos_values[mask]
                
                ax.plot(filtered_energies, filtered_dos, 
                       color=self.line_color_var.get(),
                       linewidth=self.line_width_var.get(),
                       label='Total DOS')
                
                if self.show_fermi_var.get():
                    ax.axvline(x=0, color=self.fermi_color_var.get(), 
                              linestyle='--', alpha=0.7, linewidth=2, 
                              label='Fermi Level')
                
                ax.set_xlabel('Energy (eV)', fontsize=self.font_size_var.get())
                ax.set_ylabel('Density of States (states/eV)', fontsize=self.font_size_var.get())
                ax.set_title('VASP Density of States', fontsize=self.title_font_size_var.get(), fontweight='bold')
                
                if self.show_grid_var.get():
                    ax.grid(True, alpha=self.grid_alpha_var.get())
                
                ax.legend()
                ax.set_xlim(energy_min, energy_max)
                
                fig.tight_layout()
                fig.savefig(file_path, dpi=self.dpi_var.get(), bbox_inches='tight')
                
                messagebox.showinfo("Success", f"Plot saved to {file_path}")
                self.status_var.set(f"Plot saved to {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plot: {str(e)}")
                
    def export_data(self):
        """Export filtered data to CSV"""
        if self.energies is None:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                energy_min = self.energy_min_var.get()
                energy_max = self.energy_max_var.get()
                mask = (self.energies >= energy_min) & (self.energies <= energy_max)
                filtered_energies = self.energies[mask]
                filtered_dos = self.dos_values[mask]
                
                with open(file_path, 'w') as f:
                    f.write("Energy(eV),DOS(states/eV)\n")
                    for energy, dos in zip(filtered_energies, filtered_dos):
                        f.write(f"{energy:.6f},{dos:.6f}\n")
                
                messagebox.showinfo("Success", f"Data exported to {file_path}")
                self.status_var.set(f"Data exported to {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
                
    def copy_plot(self):
        """Copy plot to clipboard"""
        messagebox.showinfo("Info", "Plot copied to clipboard functionality would be implemented here")
        
    def reset_settings(self):
        """Reset all settings to defaults"""
        self.energy_min_var.set(-7.0)
        self.energy_max_var.set(7.0)
        self.line_width_var.set(2.0)
        self.line_color_var.set('blue')
        self.fermi_color_var.set('red')
        self.grid_alpha_var.set(0.3)
        self.figure_width_var.set(12.0)
        self.figure_height_var.set(8.0)
        self.dpi_var.set(300)
        self.font_size_var.set(12)
        self.title_font_size_var.set(16)
        self.show_fermi_var.set(True)
        self.show_grid_var.set(True)
        
    def load_settings(self):
        """Load settings from file"""
        file_path = filedialog.askopenfilename(
            title="Load Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Info", "Settings loading functionality would be implemented here")
            
    def save_settings(self):
        """Save settings to file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Info", "Settings saving functionality would be implemented here")
            
    def show_about(self):
        """Show concise about dialog with author information and mascot"""
        # Create a new window for the about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title("About VASP DOS Plotter")
        about_window.geometry("500x550")
        about_window.configure(bg='#f0f0f0')
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(about_window, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="VASP DOS Plotter", 
                              font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(main_frame, text="Professional Edition v1.0", 
                                 font=('Arial', 10, 'italic'), bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 15))
        
        # Author section with photo
        author_frame = tk.Frame(main_frame, bg='#f0f0f0')
        author_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Try to load and display the mascot/author photo with proper aspect ratio
        try:
            mascot_path = os.path.join("RES", "Mascot.jpg")
            if os.path.exists(mascot_path):
                # Load the image and maintain aspect ratio
                image = Image.open(mascot_path)
                # Calculate new size maintaining aspect ratio (max 100px)
                original_width, original_height = image.size
                max_size = 100
                
                if original_width > original_height:
                    new_width = max_size
                    new_height = int((original_height * max_size) / original_width)
                else:
                    new_height = max_size
                    new_width = int((original_width * max_size) / original_height)
                
                # Resize with aspect ratio preserved
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Display the image
                image_label = tk.Label(author_frame, image=photo, bg='#f0f0f0')
                image_label.image = photo  # Keep a reference
                image_label.pack(pady=(0, 8))
            else:
                # Fallback if image not found
                image_label = tk.Label(author_frame, text="👨‍🔬", font=('Arial', 50), bg='#f0f0f0')
                image_label.pack(pady=(0, 8))
        except Exception as e:
            # Fallback if PIL not available or image loading fails
            image_label = tk.Label(author_frame, text="👨‍🔬", font=('Arial', 50), bg='#f0f0f0')
            image_label.pack(pady=(0, 8))
        
        # Author information (concise)
        author_name = tk.Label(author_frame, text="👋 Zeinab H. Fard", 
                              font=('Arial', 13, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        author_name.pack(pady=(0, 3))
        
        author_title = tk.Label(author_frame, text="Ph.D. Researcher, Chemical & Biological Engineering", 
                               font=('Arial', 9), bg='#f0f0f0', fg='#34495e')
        author_title.pack(pady=(0, 2))
        
        author_uni = tk.Label(author_frame, text="Iowa State University", 
                             font=('Arial', 9, 'bold'), bg='#f0f0f0', fg='#e74c3c')
        author_uni.pack(pady=(0, 8))
        
        # Author description (concise)
        author_desc = tk.Label(author_frame, 
                              text="Developing software tools for computational chemistry,\nDFT simulations, and data visualization.",
                              font=('Arial', 9), bg='#f0f0f0', fg='#2c3e50', justify=tk.CENTER)
        author_desc.pack(pady=(0, 15))
        
        # Project information (concise)
        project_frame = tk.Frame(main_frame, bg='#f0f0f0')
        project_frame.pack(fill=tk.X, pady=(0, 15))
        
        project_title = tk.Label(project_frame, text="About This Tool", 
                                font=('Arial', 11, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        project_title.pack(pady=(0, 8))
        
        project_text = """A comprehensive tool for plotting VASP Density of States data
with an intuitive graphical interface.

Key Features:
• Real-time plot updates with interactive sliders
• Multiple export formats (PNG, PDF, SVG)
• Professional quality output for publications
• Easy file management and batch processing

License: MIT Open Source"""
        
        project_label = tk.Label(project_frame, text=project_text, 
                                font=('Arial', 9), bg='#f0f0f0', fg='#2c3e50', justify=tk.LEFT)
        project_label.pack(pady=(0, 10))
        
        # Mission statement (concise)
        mission_text = """Making complex scientific tools accessible through\nopen-source solutions."""
        
        mission_label = tk.Label(project_frame, text=mission_text, 
                                font=('Arial', 9, 'italic'), bg='#f0f0f0', fg='#7f8c8d', justify=tk.CENTER)
        mission_label.pack(pady=(0, 15))
        
        # Close button
        close_button = tk.Button(main_frame, text="Close", command=about_window.destroy,
                                font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                relief=tk.FLAT, padx=20, pady=5)
        close_button.pack(pady=(10, 0))
        
        # Focus on the new window
        about_window.focus_set()
        
    def show_help(self):
        """Show help dialog"""
        help_text = """User Guide:

1. File Operations:
   • Use 'Browse' to select DOS files
   • 'Load RES/DOS0' for quick access to default file
   • 'Load Sample' for demonstration data

2. Energy Range:
   • Set min/max energy bounds
   • Use 'Auto-detect Range' for optimal view
   • 'Zoom to Data' shows full range

3. Appearance:
   • Customize line width, color, and style
   • Adjust grid and font settings
   • Toggle Fermi level display

4. Export:
   • Save plots in PNG, PDF, or SVG
   • Export data as CSV
   • Adjust figure size and DPI

5. Plot Controls:
   • 'Update Plot' applies current settings
   • 'Reset View' returns to auto-detected range
   • Real-time updates as you change settings"""
        
        messagebox.showinfo("User Guide", help_text)
        
    # Bulk operations methods
    def add_bulk_files(self):
        """Add files to multi-file plotting list"""
        file_paths = filedialog.askopenfilenames(
            title="Select DOS Files for Multi-File Plotting",
            filetypes=[("DOS files (no extension)", "*."), ("All files", "*.*"), ("Text files", "*.txt")]
        )
        
        for file_path in file_paths:
            if file_path not in self.bulk_files_listbox.get(0, tk.END):
                self.bulk_files_listbox.insert(tk.END, file_path)
        
        self.bulk_progress_var.set(f"Added {len(file_paths)} files. Total: {self.bulk_files_listbox.size()}")
        
    def clear_bulk_files(self):
        """Clear all files from multi-file plotting list"""
        self.bulk_files_listbox.delete(0, tk.END)
        self.bulk_progress_var.set("File list cleared")
        
    def remove_selected_bulk_files(self):
        """Remove selected files from multi-file plotting list"""
        selected_indices = self.bulk_files_listbox.curselection()
        for index in reversed(selected_indices):
            self.bulk_files_listbox.delete(index)
        
        remaining = self.bulk_files_listbox.size()
        self.bulk_progress_var.set(f"Removed {len(selected_indices)} files. Remaining: {remaining}")
        
    def plot_all_files_together(self):
        """Plot all selected files together in one plot with different colors"""
        if self.bulk_files_listbox.size() == 0:
            messagebox.showwarning("Warning", "No files selected for multi-file plotting")
            return
            
        # Start multi-file plotting in a separate thread
        self.bulk_progress_var.set("Loading files for multi-file plot...")
        
        def multi_plot_thread():
            try:
                file_paths = [self.bulk_files_listbox.get(i) for i in range(self.bulk_files_listbox.size())]
                file_data = []
                
                # Load all files
                for i, file_path in enumerate(file_paths):
                    self.root.after(0, lambda f=file_path, idx=i+1, tot=len(file_paths): 
                                  self.bulk_progress_var.set(f"Loading {idx}/{tot}: {os.path.basename(f)}"))
                    
                    try:
                        energies, dos_values = self.read_dos_file(file_path)
                        if len(energies) > 0:
                            file_data.append((energies, dos_values, file_path))
                    except Exception as e:
                        print(f"Error loading {file_path}: {str(e)}")
                
                if not file_data:
                    self.root.after(0, lambda: messagebox.showerror("Error", "No valid files could be loaded"))
                    return
                
                # Create multi-file plot in main thread
                self.root.after(0, lambda: self.create_multi_file_plot(file_data))
                
            except Exception as e:
                self.root.after(0, lambda: self.bulk_progress_var.set(f"Multi-file plotting error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Multi-file plotting failed: {str(e)}"))
        
        threading.Thread(target=multi_plot_thread, daemon=True).start()
        
    def create_multi_file_plot(self, file_data):
        """Create a multi-file plot with different colors and legend"""
        try:
            self.bulk_progress_var.set("Creating multi-file plot...")
            
            # Set plotting mode to multi-file and store data
            self.plotting_mode = "multi"
            self.multi_file_data = file_data
            
            # Get current settings
            energy_min = float(self.energy_min_var.get())
            energy_max = float(self.energy_max_var.get())
            
            # Clear current plot
            self.ax.clear()
            
            # Generate colors based on scheme
            colors = self.generate_colors(len(file_data))
            
            # Plot each file with different color
            for i, (energies, dos_values, file_path) in enumerate(file_data):
                # Filter data
                mask = (energies >= energy_min) & (energies <= energy_max)
                filtered_energies = energies[mask]
                filtered_dos = dos_values[mask]
                
                if len(filtered_energies) > 0:
                    # Format legend label with path information
                    legend_label = self.format_legend_label(file_path)
                    
                    # Plot with unique color and formatted path as label
                    self.ax.plot(filtered_energies, filtered_dos, 
                               color=colors[i],
                               linewidth=self.line_width_var.get(),
                               label=legend_label)
            
            # Add Fermi level if enabled
            if self.show_fermi_var.get():
                self.ax.axvline(x=0, color=self.fermi_color_var.get(), 
                               linestyle='--', alpha=0.7, linewidth=2, 
                               label='Fermi Level')
            
            # Customize plot
            self.ax.set_xlabel('Energy (eV)', fontsize=self.font_size_var.get())
            self.ax.set_ylabel('Density of States (states/eV)', fontsize=self.font_size_var.get())
            self.ax.set_title('Multi-File DOS Comparison', fontsize=self.title_font_size_var.get(), fontweight='bold')
            
            if self.show_grid_var.get():
                self.ax.grid(True, alpha=self.grid_alpha_var.get())
            
            # Add legend
            self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            self.ax.set_xlim(energy_min, energy_max)
            
            # Auto-scale y-axis based on all data
            all_dos_values = []
            for energies, dos_values, _ in file_data:
                mask = (energies >= energy_min) & (energies <= energy_max)
                filtered_dos = dos_values[mask]
                if len(filtered_dos) > 0:
                    all_dos_values.extend(filtered_dos)
            
            if all_dos_values:
                y_margin = (max(all_dos_values) - min(all_dos_values)) * 0.05
                self.ax.set_ylim(min(all_dos_values) - y_margin, max(all_dos_values) + y_margin)
            
            self.canvas.draw()
            
            # Update status
            self.status_var.set(f"Multi-file plot created with {len(file_data)} files")
            self.bulk_progress_var.set(f"Multi-file plot complete: {len(file_data)} files plotted")
            
        except Exception as e:
            self.bulk_progress_var.set(f"Error creating multi-file plot: {str(e)}")
            messagebox.showerror("Error", f"Failed to create multi-file plot: {str(e)}")
            
    def generate_colors(self, num_colors):
        """Generate distinct colors for multiple files"""
        import matplotlib.cm as cm
        import matplotlib.colors as mcolors
        
        scheme = self.color_scheme_var.get()
        
        if scheme == 'auto':
            # Use matplotlib's default color cycle
            colors = [f'C{i}' for i in range(num_colors)]
        elif scheme == 'rainbow':
            colors = [cm.rainbow(i / max(1, num_colors - 1)) for i in range(num_colors)]
        elif scheme == 'viridis':
            colors = [cm.viridis(i / max(1, num_colors - 1)) for i in range(num_colors)]
        elif scheme == 'plasma':
            colors = [cm.plasma(i / max(1, num_colors - 1)) for i in range(num_colors)]
        elif scheme == 'tab10':
            colors = [cm.tab10(i % 10) for i in range(num_colors)]
        else:
            # Fallback to default
            colors = [f'C{i}' for i in range(num_colors)]
            
        return colors
        
    def format_legend_label(self, file_path):
        """Format file path for legend display"""
        import os
        
        # Get current working directory
        cwd = os.getcwd()
        
        # Make path relative to current directory if possible
        try:
            rel_path = os.path.relpath(file_path, cwd)
            if not rel_path.startswith('..'):
                # Path is within current directory, use relative path
                display_path = rel_path
            else:
                # Path is outside current directory, use absolute path
                display_path = file_path
        except ValueError:
            # Can't make relative path (different drives on Windows), use absolute
            display_path = file_path
        
        # Trim long paths with ellipsis
        max_length = 50  # Maximum characters for legend label
        if len(display_path) > max_length:
            # Find a good place to cut (prefer cutting at path separators)
            cut_point = max_length - 3  # Leave room for "..."
            
            # Try to cut at a path separator
            for i in range(cut_point, max(0, cut_point - 10), -1):
                if display_path[i] in ['/', '\\']:
                    cut_point = i
                    break
            
            display_path = display_path[:cut_point] + "..."
        
        return display_path
        
    def clear_multi_plot(self):
        """Clear the multi-file plot"""
        self.ax.clear()
        self.ax.set_title('VASP Density of States', fontsize=self.title_font_size_var.get(), fontweight='bold')
        self.canvas.draw()
        
        # Reset plotting mode
        self.plotting_mode = "single"
        self.multi_file_data = []
        
        self.bulk_progress_var.set("Plot cleared")
        self.status_var.set("Ready")
        
    def save_multi_plot(self):
        """Save the current multi-file plot"""
        if not hasattr(self, 'ax') or not self.ax.lines:
            messagebox.showwarning("Warning", "No multi-file plot to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Multi-File Plot",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")]
        )
        
        if file_path:
            try:
                # Create new figure with export settings
                fig = Figure(figsize=(self.figure_width_var.get(), self.figure_height_var.get()), 
                            dpi=self.dpi_var.get())
                ax = fig.add_subplot(111)
                
                # Recreate the multi-file plot
                energy_min = float(self.energy_min_var.get())
                energy_max = float(self.energy_max_var.get())
                
                # Get all data from current plot
                file_data = []
                for line in self.ax.lines:
                    if line.get_label() != 'Fermi Level':
                        # We need to get the original data, but we'll work with what we have
                        x_data, y_data = line.get_data()
                        label = line.get_label()
                        color = line.get_color()
                        file_data.append((x_data, y_data, label, color))
                
                # Plot each file
                for x_data, y_data, label, color in file_data:
                    ax.plot(x_data, y_data, color=color, linewidth=self.line_width_var.get(), label=label)
                
                # Add Fermi level if present
                for line in self.ax.lines:
                    if line.get_label() == 'Fermi Level':
                        ax.axvline(x=0, color=line.get_color(), linestyle='--', alpha=0.7, linewidth=2, label='Fermi Level')
                        break
                
                # Customize plot
                ax.set_xlabel('Energy (eV)', fontsize=self.font_size_var.get())
                ax.set_ylabel('Density of States (states/eV)', fontsize=self.font_size_var.get())
                ax.set_title('Multi-File DOS Comparison', fontsize=self.title_font_size_var.get(), fontweight='bold')
                
                if self.show_grid_var.get():
                    ax.grid(True, alpha=self.grid_alpha_var.get())
                
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.set_xlim(energy_min, energy_max)
                
                # Copy y-axis limits
                ax.set_ylim(self.ax.get_ylim())
                
                fig.tight_layout()
                fig.savefig(file_path, dpi=self.dpi_var.get(), bbox_inches='tight')
                
                messagebox.showinfo("Success", f"Multi-file plot saved to {file_path}")
                self.status_var.set(f"Multi-file plot saved to {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save multi-file plot: {str(e)}")

def main():
    """Main function"""
    root = tk.Tk()
    app = DOSPlotterGUI(root)
    
    # Try to load default file if it exists
    if os.path.exists("RES/DOS0"):
        app.load_file("RES/DOS0")
    
    root.mainloop()

if __name__ == "__main__":
    main()

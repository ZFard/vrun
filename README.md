# VASP DOS Plotting Project

This project demonstrates how to create Density of States (DOS) plots using VASP output files (vasprun.xml) and provides multiple plotting options.

## Project Structure

```
vrun/
├── dos_plotter_gui.py   # Main GUI application (recommended)
├── plot_real_dos.py     # Real VASP DOS data plotting script
├── launch_gui.bat       # Windows launcher for GUI
├── requirements.txt     # Python package requirements
├── README.md           # This documentation
├── GUI_USAGE_GUIDE.md  # Detailed GUI usage guide
├── RES/
│   └── DOS0            # Real VASP DOS data file
└── venv/               # Python virtual environment
```

## Setup Instructions

### Option 1: Using Virtual Environment (Recommended)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: System-wide Installation

Install packages directly to your system Python:
```bash
pip install pymatgen matplotlib numpy
```

## Usage

### Method 1: GUI Application (Recommended)

Launch the intuitive graphical interface:

```bash
python dos_plotter_gui.py
```

Or use the launcher:
```bash
launch_gui.bat
```

**GUI Features:**
- 📁 **File Management**: Browse and load DOS files easily
- ⚙️ **Customizable Settings**: Adjust energy range, colors, fonts, and more
- 📊 **Real-time Plotting**: See changes instantly as you adjust settings
- 💾 **Multiple Export Options**: Save plots as PNG, PDF, SVG or export data as CSV
- 🎯 **Smart Defaults**: Auto-detect optimal energy ranges
- 📈 **Professional Output**: High-quality plots suitable for publications

### Method 2: Command Line Script

For automated or batch processing:

```bash
python plot_real_dos.py
```

This script:
- Reads real VASP DOS files (like `RES/DOS0`)
- Creates professional plots with -7 to 7 eV bounds
- Provides detailed statistics
- Saves filtered data for further analysis

## Understanding the Output

### DOS Plot Features

- **Energy Axis**: Typically in eV, with Fermi level at 0 eV
- **DOS Axis**: Density of states in states/eV
- **Fermi Level**: Marked with a red dashed line
- **Peaks**: Represent electronic states at specific energies

### Sample Data

The included `vasprun.xml` contains:
- A simple hydrogen atom system
- Energy eigenvalues from -5 to 4 eV
- DOS data with Gaussian-like peaks
- Fermi level at 0 eV

## Troubleshooting

### Common Issues

1. **ImportError for numpy/matplotlib**: 
   - Try installing with `--user` flag: `pip install --user numpy matplotlib`
   - Or use the basic plotting script that doesn't require external packages

2. **VASP file parsing errors**:
   - The script will fall back to synthetic data
   - Ensure your vasprun.xml is complete and properly formatted

3. **Virtual environment issues**:
   - Use the basic plotting script as a fallback
   - Or install packages system-wide

### Alternative Plotting Methods

If Python plotting doesn't work, you can:

1. **Use the generated data file**:
   - Import `dos_data.txt` into Excel, Origin, or other plotting software
   - Columns are: Energy(eV) and DOS(states/eV)

2. **Use Gnuplot**:
   - Install Gnuplot from https://gnuplot.info/
   - Run: `gnuplot plot_dos.gp`

3. **Use online plotting tools**:
   - Upload `dos_data.txt` to online plotting services
   - Many scientific plotting websites accept tab-delimited data

## GUI Application Features

### 📁 File Management
- **Browse Files**: Easy file selection with dialog
- **Quick Load**: One-click loading of `RES/DOS0` or sample data
- **File Info**: Display data statistics and file details
- **Multiple Formats**: Support for various DOS file formats

### ⚙️ Customizable Settings
- **Energy Range**: Adjustable min/max bounds with auto-detection
- **Line Properties**: Width, color, and style customization
- **Fermi Level**: Toggle display with color options
- **Grid Settings**: Show/hide grid with transparency control
- **Font Control**: Adjustable font sizes for labels and titles

### 📊 Real-time Plotting
- **Live Updates**: See changes instantly as you adjust settings
- **Interactive Controls**: Zoom, reset view, and auto-detect ranges
- **Professional Display**: High-quality matplotlib integration
- **Status Updates**: Real-time feedback on operations

### 💾 Export Options
- **Multiple Formats**: PNG, PDF, SVG support
- **High Resolution**: Adjustable DPI up to 600
- **Custom Sizing**: Flexible figure dimensions
- **Data Export**: CSV format for further analysis
- **Settings Save/Load**: Preserve your preferences

### 🎯 Smart Features
- **Auto-detect Range**: Automatically find optimal energy bounds
- **Zoom to Data**: Quick view of full data range
- **Reset View**: Return to default settings
- **Error Handling**: Graceful handling of file issues

## File Descriptions

- **dos_plotter_gui.py**: Main GUI application with interactive sliders and real-time updates
- **plot_real_dos.py**: Command-line script for real VASP DOS data plotting
- **launch_gui.bat**: Windows launcher for the GUI application
- **requirements.txt**: Python package dependencies
- **README.md**: This documentation file
- **GUI_USAGE_GUIDE.md**: Detailed guide for using the GUI application
- **RES/DOS0**: Real VASP DOS data file (your actual data)
- **venv/**: Python virtual environment with all dependencies

## Requirements

### For Full Functionality
- Python 3.7+
- pymatgen
- matplotlib
- numpy

### For Basic Functionality
- Python 3.7+ (built-in libraries only)

### Optional
- Gnuplot (for alternative plotting)

## Example Output

The basic script produces a text-based plot showing:
```
Density of States Plot (Text-based)
==================================================
Energy (eV)    |    DOS (states/eV)
--------------------------------------------------
  -10.00     |  0.000
   -8.99     |  0.000
   -7.99     |  0.011
   -6.98     | ████ 0.139
   -5.98     | ██████████████████ 0.619
   -4.97     | ██████████████████████████████ 1.002
  ...
```

This provides a visual representation of the DOS even without graphical plotting libraries.

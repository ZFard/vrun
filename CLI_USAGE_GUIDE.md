# VASP DOS Plotter - Command Line Interface Guide

A comprehensive guide for using the VASP DOS Plotter from the command line.

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Basic Commands](#basic-commands)
- [Single File Plotting](#single-file-plotting)
- [Multi-File Plotting](#multi-file-plotting)
- [Advanced Options](#advanced-options)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

The simplest way to plot a DOS file:

```bash
# Using the plotter module directly
python vasp_dos_plotter/plotter.py quick your_dos_file.txt

# Or using the standalone CLI script
python vasp_dos_cli.py quick your_dos_file.txt

# Demo mode (plots RES/DOS0 if available)
python vasp_dos_plotter/plotter.py
```

This creates a plot with default settings and displays it on screen.

## Installation

Make sure you have the required dependencies installed:

```bash
pip install numpy matplotlib pillow
```

## Basic Commands

### Command Structure
```bash
# Using the standalone CLI script
python vasp_dos_cli.py <command> [options]

# Using the plotter module directly
python vasp_dos_plotter/plotter.py <command> [options]

# Using as a module
python -m vasp_dos_plotter.plotter <command> [options]
```

### Available Commands
- `quick` - Quick plot with default settings
- `plot` - Advanced plotting with full customization
  - `single` - Plot single DOS file
  - `multi` - Plot multiple DOS files

## Single File Plotting

### Basic Single File Plot
```bash
python vasp_dos_cli.py plot single your_file.txt
```

### Save to File
```bash
python vasp_dos_cli.py plot single your_file.txt -o output.png
```

### Custom Energy Range
```bash
python vasp_dos_cli.py plot single your_file.txt -r -5 5 -o plot.png
```

### Full Customization
```bash
python vasp_dos_cli.py plot single your_file.txt \
  -r -10 10 \
  -o publication_plot.png \
  --color red \
  --width 3 \
  --fermi-color green \
  --dpi 600 \
  --size 12 8
```

### Single File Options

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --range MIN MAX` | Energy range in eV | -7 7 |
| `-o, --output` | Output file path | Display on screen |
| `--color` | Line color | blue |
| `--width` | Line width | 2 |
| `--no-fermi` | Hide Fermi level | Show Fermi level |
| `--fermi-color` | Fermi level color | red |
| `--no-grid` | Hide grid | Show grid |
| `--dpi` | Output DPI | 300 |
| `--size WIDTH HEIGHT` | Figure size | 12 8 |

## Multi-File Plotting

### Basic Multi-File Plot
```bash
python vasp_dos_cli.py plot multi file1.txt file2.txt file3.txt
```

### Multi-File with Custom Settings
```bash
python vasp_dos_cli.py plot multi *.txt -r -10 10 -c rainbow -o comparison.png
```

### Advanced Multi-File Plot
```bash
python vasp_dos_cli.py plot multi file1.txt file2.txt \
  -r -8 8 \
  -o multi_plot.pdf \
  -c viridis \
  --width 2.5 \
  --dpi 300 \
  --size 14 10
```

### Multi-File Options

All single file options plus:

| Option | Description | Default |
|--------|-------------|---------|
| `-c, --color-scheme` | Color scheme for multiple files | auto |
| | Choices: auto, rainbow, viridis, plasma, tab10 | |

## Advanced Options

### Color Schemes for Multi-File Plots
- `auto` - Matplotlib default color cycle
- `rainbow` - Rainbow color spectrum
- `viridis` - Viridis colormap (perceptually uniform)
- `plasma` - Plasma colormap
- `tab10` - Tableau 10-color palette

### Output Formats
Supported formats: PNG, PDF, SVG, EPS, PS

### Energy Range
- Specify as two numbers: `-r -5 5`
- Range is in electron volts (eV)
- Fermi level is always at 0 eV

### Figure Size
- Specify as width and height: `--size 12 8`
- Units are in inches
- Larger sizes for publication-quality plots

## Examples

### Example 1: Quick Publication Plot
```bash
python vasp_dos_cli.py plot single RES/DOS0 \
  -r -5 5 \
  -o publication_dos.png \
  --color black \
  --width 2 \
  --dpi 600 \
  --size 10 6
```

### Example 2: Compare Multiple Structures
```bash
python vasp_dos_cli.py plot multi \
  RES/clean/DOS0 \
  RES/H-bridge/DOS0 \
  RES/O-vac/DOS0 \
  -r -8 8 \
  -o structure_comparison.png \
  -c rainbow \
  --width 2.5
```

### Example 3: Batch Processing
```bash
# Plot all DOS files in subdirectories
python vasp_dos_cli.py plot multi RES/*/DOS0 -o all_structures.png

# Plot with wildcards
python vasp_dos_cli.py plot multi *.txt -r -10 10 -o batch_plot.png
```

### Example 4: Custom Styling
```bash
python vasp_dos_cli.py plot single my_dos.txt \
  -r -6 6 \
  -o styled_plot.png \
  --color "#2E86AB" \
  --width 3 \
  --fermi-color "#A23B72" \
  --no-grid \
  --dpi 300 \
  --size 12 8
```

### Example 5: High-Resolution Export
```bash
python vasp_dos_cli.py plot single data.txt \
  -o high_res.pdf \
  --dpi 600 \
  --size 16 12
```

## File Format

The CLI expects DOS files in the following format:
```
# Energy Total_DOS Spin_Up Spin_Down Integrated_Up Integrated_Down
-10.000000  0.000123  0.000061  0.000062  0.000000  0.000000
-9.949749  0.000135  0.000067  0.000068  0.000001  0.000001
...
```

- First column: Energy in eV
- Second column: Total DOS (used for plotting)
- Comments (lines starting with #) are ignored
- Empty lines are ignored

## Troubleshooting

### Common Issues

#### 1. File Not Found
```
Error: No valid data found in file
```
**Solution**: Check file path and format. Ensure file contains numeric data.

#### 2. No Data in Range
```
No data in selected range
```
**Solution**: Adjust energy range with `-r` option or check data range.

#### 3. Import Error
```
ModuleNotFoundError: No module named 'matplotlib'
```
**Solution**: Install required dependencies:
```bash
pip install numpy matplotlib pillow
```

#### 4. Permission Error
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check write permissions for output directory.

### Debug Mode
For detailed error information, run with verbose output:
```bash
python -u vasp_dos_cli.py plot single file.txt -o output.png
```

### Getting Help
```bash
# General help
python vasp_dos_cli.py --help

# Command-specific help
python vasp_dos_cli.py plot --help
python vasp_dos_cli.py plot single --help
python vasp_dos_cli.py plot multi --help
python vasp_dos_cli.py quick --help
```

## Tips and Best Practices

### 1. Energy Range Selection
- Use `-r -5 5` for most DOS plots
- Use `-r -10 10` for wide energy ranges
- Use `-r -2 2` for detailed Fermi level analysis

### 2. Output Quality
- Use `--dpi 300` for screen viewing
- Use `--dpi 600` for publications
- Use `--size 12 8` for standard plots
- Use `--size 16 12` for large displays

### 3. Multi-File Plots
- Use `-c rainbow` for colorful comparisons
- Use `-c viridis` for scientific publications
- Use `-c auto` for default matplotlib colors

### 4. File Organization
```bash
# Organize by structure
python vasp_dos_cli.py plot multi \
  structures/clean/DOS0 \
  structures/h_bridge/DOS0 \
  structures/o_vacancy/DOS0 \
  -o structure_comparison.png

# Organize by calculation
python vasp_dos_cli.py plot multi \
  calculations/relaxed/DOS0 \
  calculations/unrelaxed/DOS0 \
  -o relaxation_effect.png
```

### 5. Batch Processing
```bash
# Process all files in directory
for file in *.txt; do
  python vasp_dos_cli.py quick "$file" -o "${file%.txt}_plot.png"
done

# Process with different settings
python vasp_dos_cli.py plot multi *.txt -r -5 5 -o batch_plot.png
```

## Integration with Scripts

### Python Script Example
```python
import subprocess
import os

def plot_dos_files(file_list, output_dir):
    """Plot multiple DOS files using CLI"""
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in file_list:
        output_file = os.path.join(output_dir, f"{os.path.basename(file_path)}_plot.png")
        
        cmd = [
            "python", "vasp_dos_cli.py", "plot", "single",
            file_path, "-o", output_file, "-r", "-5", "5"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Plotted {file_path}")
        else:
            print(f"✗ Error plotting {file_path}: {result.stderr}")

# Usage
files = ["file1.txt", "file2.txt", "file3.txt"]
plot_dos_files(files, "plots")
```

### Bash Script Example
```bash
#!/bin/bash
# batch_plot.sh - Plot all DOS files in current directory

for file in *.txt; do
    if [ -f "$file" ]; then
        echo "Plotting $file..."
        python vasp_dos_cli.py quick "$file" -o "${file%.txt}_plot.png"
    fi
done

echo "Batch plotting complete!"
```

## Performance Tips

1. **Large Files**: For files with >10,000 points, consider using `-r` to limit range
2. **Multiple Files**: Use `plot multi` instead of multiple `plot single` commands
3. **High DPI**: Only use `--dpi 600` when necessary for final output
4. **Memory**: Large multi-file plots may require more memory

## Support

For issues and questions:
- Check this guide first
- Use `--help` for command-specific information
- Ensure file format matches expected structure
- Verify all dependencies are installed

---

**Happy Plotting!** 🎨📊

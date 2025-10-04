# VASP DOS Plotter - CLI Quick Reference

## Quick Commands

### Basic Plotting
```bash
# Quick plot (simplest) - using plotter directly
python vasp_dos_plotter/plotter.py quick file.txt

# Quick plot with output
python vasp_dos_plotter/plotter.py quick file.txt -o plot.png

# Demo mode (plots RES/DOS0 if available)
python vasp_dos_plotter/plotter.py

# Alternative: using standalone CLI script
python vasp_dos_cli.py quick file.txt
```

### Single File Plotting
```bash
# Basic single file
python vasp_dos_plotter/plotter.py plot single file.txt

# Custom range and output
python vasp_dos_plotter/plotter.py plot single file.txt -r -5 5 -o plot.png

# Full customization
python vasp_dos_plotter/plotter.py plot single file.txt -r -5 5 -o plot.png --color red --width 3 --dpi 600
```

### Multi-File Plotting
```bash
# Basic multi-file
python vasp_dos_plotter/plotter.py plot multi file1.txt file2.txt file3.txt

# With custom settings
python vasp_dos_plotter/plotter.py plot multi *.txt -r -10 10 -c rainbow -o comparison.png
```

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `-r, --range MIN MAX` | Energy range | `-r -5 5` |
| `-o, --output` | Output file | `-o plot.png` |
| `--color` | Line color | `--color red` |
| `--width` | Line width | `--width 3` |
| `--no-fermi` | Hide Fermi level | `--no-fermi` |
| `--fermi-color` | Fermi color | `--fermi-color green` |
| `--no-grid` | Hide grid | `--no-grid` |
| `--dpi` | Output DPI | `--dpi 600` |
| `--size W H` | Figure size | `--size 12 8` |
| `-c, --color-scheme` | Multi-file colors | `-c rainbow` |

## Color Schemes (Multi-File)
- `auto` - Default colors
- `rainbow` - Rainbow spectrum
- `viridis` - Scientific colormap
- `plasma` - Plasma colormap
- `tab10` - Tableau colors

## Common Examples

### Publication Plot
```bash
python vasp_dos_cli.py plot single data.txt \
  -r -5 5 -o pub_plot.png \
  --color black --width 2 --dpi 600 --size 10 6
```

### Structure Comparison
```bash
python vasp_dos_cli.py plot multi \
  clean/DOS0 h_bridge/DOS0 o_vac/DOS0 \
  -r -8 8 -o comparison.png -c rainbow
```

### Batch Processing
```bash
python vasp_dos_cli.py plot multi *.txt -r -10 10 -o batch.png
```

## Help Commands
```bash
# Using plotter directly
python vasp_dos_plotter/plotter.py --help
python vasp_dos_plotter/plotter.py plot --help
python vasp_dos_plotter/plotter.py plot single --help
python vasp_dos_plotter/plotter.py plot multi --help
python vasp_dos_plotter/plotter.py quick --help

# Using standalone CLI script
python vasp_dos_cli.py --help
```

## File Format
```
# Energy Total_DOS Spin_Up Spin_Down
-10.000000  0.000123  0.000061  0.000062
-9.949749  0.000135  0.000067  0.000068
...
```

## Troubleshooting
- **No data found**: Check file format and path
- **No data in range**: Adjust `-r` range
- **Import error**: Install dependencies with `pip install numpy matplotlib pillow`
- **Permission error**: Check write permissions

---
*For detailed information, see CLI_USAGE_GUIDE.md*

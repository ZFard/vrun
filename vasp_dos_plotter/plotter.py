#!/usr/bin/env python3
"""
Plot real DOS data from VASP RES/DOS0 file
Enhanced with GUI plotting functionality
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.cm as cm
import matplotlib.colors as mcolors

def read_dos_file(filename="RES/DOS0"):
    """
    Read DOS data from VASP DOS file
    Format: Energy Total_DOS Spin_Up Spin_Down Integrated_Up Integrated_Down
    """
    energies = []
    total_dos = []
    
    print(f"Reading DOS data from {filename}...")
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                try:
                    energy = float(parts[0])
                    dos_value = float(parts[1])  # Total DOS
                    energies.append(energy)
                    total_dos.append(dos_value)
                except ValueError:
                    continue
    
    return np.array(energies), np.array(total_dos)

def plot_dos_real(energies, dos_values, energy_range=(-7, 7), save_plot=True):
    """
    Plot real DOS data with specified energy range
    """
    # Filter data to the specified energy range
    mask = (energies >= energy_range[0]) & (energies <= energy_range[1])
    filtered_energies = energies[mask]
    filtered_dos = dos_values[mask]
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.plot(filtered_energies, filtered_dos, 'b-', linewidth=2, label='Total DOS')
    
    # Add Fermi level line at 0 eV
    plt.axvline(x=0, color='r', linestyle='--', alpha=0.7, linewidth=2, label='Fermi Level')
    
    # Customize the plot
    plt.xlabel('Energy (eV)', fontsize=14)
    plt.ylabel('Density of States (states/eV)', fontsize=14)
    plt.title('Real VASP Density of States Plot', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Set energy range
    plt.xlim(energy_range[0], energy_range[1])
    
    # Add some styling
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('real_dos_plot.png', dpi=300, bbox_inches='tight')
        print(f"Real DOS plot saved as 'real_dos_plot.png'")
    
    plt.show()
    
    # Print statistics
    print(f"\nReal DOS Data Statistics:")
    print(f"Energy range: {filtered_energies.min():.3f} to {filtered_energies.max():.3f} eV")
    print(f"Number of data points: {len(filtered_energies)}")
    print(f"Maximum DOS: {filtered_dos.max():.3f} states/eV")
    print(f"Minimum DOS: {filtered_dos.min():.3f} states/eV")
    print(f"Average DOS: {filtered_dos.mean():.3f} states/eV")
    
    # Find DOS at Fermi level (closest to 0 eV)
    fermi_idx = np.argmin(np.abs(filtered_energies))
    fermi_dos = filtered_dos[fermi_idx]
    fermi_energy = filtered_energies[fermi_idx]
    print(f"DOS at Fermi level ({fermi_energy:.3f} eV): {fermi_dos:.3f} states/eV")

def save_filtered_data(energies, dos_values, energy_range=(-7, 7), filename="filtered_dos_data.txt"):
    """
    Save filtered DOS data to a text file
    """
    mask = (energies >= energy_range[0]) & (energies <= energy_range[1])
    filtered_energies = energies[mask]
    filtered_dos = dos_values[mask]
    
    with open(filename, 'w') as f:
        f.write("Energy(eV)\tDOS(states/eV)\n")
        for energy, dos in zip(filtered_energies, filtered_dos):
            f.write(f"{energy:.6f}\t{dos:.6f}\n")
    
    print(f"Filtered DOS data saved to '{filename}'")

def plot_dos_file(file_path, energy_range=(-7, 7), output_file=None):
    """
    Plot DOS data from a file with specified energy range
    
    Args:
        file_path (str): Path to the DOS file
        energy_range (tuple): Energy range (min, max) in eV
        output_file (str): Optional output file path
    """
    energies, total_dos = read_dos_file(file_path)
    
    # Filter data within energy range
    mask = (energies >= energy_range[0]) & (energies <= energy_range[1])
    filtered_energies = energies[mask]
    filtered_dos = total_dos[mask]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_energies, filtered_dos, 'b-', linewidth=2, label='Total DOS')
    plt.axvline(x=0, color='r', linestyle='--', alpha=0.7, label='Fermi Level')
    plt.xlabel('Energy (eV)')
    plt.ylabel('Density of States (states/eV)')
    plt.title(f'Density of States - {os.path.basename(file_path)}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(energy_range)
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")
    else:
        plt.show()

def generate_colors(num_colors, color_scheme='auto'):
    """
    Generate distinct colors for multiple files
    
    Args:
        num_colors (int): Number of colors needed
        color_scheme (str): Color scheme to use ('auto', 'rainbow', 'viridis', 'plasma', 'tab10')
    
    Returns:
        list: List of color values
    """
    if color_scheme == 'auto':
        # Use matplotlib's default color cycle
        colors = [f'C{i}' for i in range(num_colors)]
    elif color_scheme == 'rainbow':
        colors = [cm.rainbow(i / max(1, num_colors - 1)) for i in range(num_colors)]
    elif color_scheme == 'viridis':
        colors = [cm.viridis(i / max(1, num_colors - 1)) for i in range(num_colors)]
    elif color_scheme == 'plasma':
        colors = [cm.plasma(i / max(1, num_colors - 1)) for i in range(num_colors)]
    elif color_scheme == 'tab10':
        colors = [cm.tab10(i % 10) for i in range(num_colors)]
    else:
        # Fallback to default
        colors = [f'C{i}' for i in range(num_colors)]
        
    return colors

def format_legend_label(file_path, max_length=50):
    """
    Format file path for legend display
    
    Args:
        file_path (str): Full file path
        max_length (int): Maximum characters for legend label
    
    Returns:
        str: Formatted legend label
    """
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

def plot_single_dos(ax, energies, dos_values, energy_min, energy_max, 
                   line_color='blue', line_width=2, show_fermi=True, 
                   fermi_color='red', show_grid=True, grid_alpha=0.3,
                   font_size=12, title_font_size=16, auto_scale=True):
    """
    Plot single file DOS data on the given axes
    
    Args:
        ax: matplotlib axes object
        energies (np.array): Energy values
        dos_values (np.array): DOS values
        energy_min (float): Minimum energy for plotting
        energy_max (float): Maximum energy for plotting
        line_color (str): Color for the DOS line
        line_width (float): Width of the DOS line
        show_fermi (bool): Whether to show Fermi level
        fermi_color (str): Color for Fermi level line
        show_grid (bool): Whether to show grid
        grid_alpha (float): Grid transparency
        font_size (int): Font size for labels
        title_font_size (int): Font size for title
        auto_scale (bool): Whether to auto-scale y-axis
    
    Returns:
        tuple: (filtered_energies, filtered_dos) for further use
    """
    # Clear axes
    ax.clear()
    
    # Filter data
    mask = (energies >= energy_min) & (energies <= energy_max)
    filtered_energies = energies[mask]
    filtered_dos = dos_values[mask]
    
    if len(filtered_energies) == 0:
        ax.text(0.5, 0.5, 'No data in selected range', 
               transform=ax.transAxes, ha='center', va='center')
        return filtered_energies, filtered_dos
    
    # Plot data
    ax.plot(filtered_energies, filtered_dos, 
            color=line_color,
            linewidth=line_width,
            label='Total DOS')
    
    # Add Fermi level
    if show_fermi:
        ax.axvline(x=0, color=fermi_color, 
                   linestyle='--', alpha=0.7, linewidth=2, 
                   label='Fermi Level')
    
    # Customize plot
    ax.set_xlabel('Energy (eV)', fontsize=font_size)
    ax.set_ylabel('Density of States (states/eV)', fontsize=font_size)
    ax.set_title('VASP Density of States', fontsize=title_font_size, fontweight='bold')
    
    if show_grid:
        ax.grid(True, alpha=grid_alpha)
    
    ax.legend()
    ax.set_xlim(energy_min, energy_max)
    
    # Auto-scale y-axis
    if auto_scale:
        y_margin = (filtered_dos.max() - filtered_dos.min()) * 0.05
        ax.set_ylim(filtered_dos.min() - y_margin, filtered_dos.max() + y_margin)
    
    return filtered_energies, filtered_dos

def plot_multi_dos(ax, multi_file_data, energy_min, energy_max,
                  line_width=2, show_fermi=True, fermi_color='red',
                  show_grid=True, grid_alpha=0.3, font_size=12, 
                  title_font_size=16, color_scheme='auto', auto_scale=True):
    """
    Plot multiple DOS files on the same axes
    
    Args:
        ax: matplotlib axes object
        multi_file_data (list): List of tuples (energies, dos_values, file_path)
        energy_min (float): Minimum energy for plotting
        energy_max (float): Maximum energy for plotting
        line_width (float): Width of the DOS lines
        show_fermi (bool): Whether to show Fermi level
        fermi_color (str): Color for Fermi level line
        show_grid (bool): Whether to show grid
        grid_alpha (float): Grid transparency
        font_size (int): Font size for labels
        title_font_size (int): Font size for title
        color_scheme (str): Color scheme for multiple files
        auto_scale (bool): Whether to auto-scale y-axis
    
    Returns:
        list: List of all DOS values for further use
    """
    # Clear axes
    ax.clear()
    
    # Generate colors based on scheme
    colors = generate_colors(len(multi_file_data), color_scheme)
    
    # Plot each file with different color
    all_dos_values = []
    for i, (energies, dos_values, file_path) in enumerate(multi_file_data):
        # Filter data
        mask = (energies >= energy_min) & (energies <= energy_max)
        filtered_energies = energies[mask]
        filtered_dos = dos_values[mask]
        
        if len(filtered_energies) > 0:
            # Format legend label with path information
            legend_label = format_legend_label(file_path)
            
            # Plot with unique color and formatted path as label
            ax.plot(filtered_energies, filtered_dos, 
                   color=colors[i],
                   linewidth=line_width,
                   label=legend_label)
            all_dos_values.extend(filtered_dos)
    
    if not all_dos_values:
        ax.text(0.5, 0.5, 'No data in selected range', 
               transform=ax.transAxes, ha='center', va='center')
        return all_dos_values
    
    # Add Fermi level if enabled
    if show_fermi:
        ax.axvline(x=0, color=fermi_color, 
                   linestyle='--', alpha=0.7, linewidth=2, 
                   label='Fermi Level')
    
    # Customize plot
    ax.set_xlabel('Energy (eV)', fontsize=font_size)
    ax.set_ylabel('Density of States (states/eV)', fontsize=font_size)
    ax.set_title('Multi-File DOS Comparison', fontsize=title_font_size, fontweight='bold')
    
    if show_grid:
        ax.grid(True, alpha=grid_alpha)
    
    # Add legend
    ax.legend()
    ax.set_xlim(energy_min, energy_max)
    
    # Auto-scale y-axis based on all data
    if auto_scale:
        y_margin = (max(all_dos_values) - min(all_dos_values)) * 0.05
        ax.set_ylim(min(all_dos_values) - y_margin, max(all_dos_values) + y_margin)
    
    return all_dos_values

def create_export_plot(fig, ax, plotting_mode, energies=None, dos_values=None, 
                      multi_file_data=None, energy_min=-7, energy_max=7,
                      line_color='blue', line_width=2, show_fermi=True, 
                      fermi_color='red', show_grid=True, grid_alpha=0.3,
                      font_size=12, title_font_size=16, color_scheme='auto'):
    """
    Create a plot for export (PNG, PDF, SVG) with high quality settings
    
    Args:
        fig: matplotlib figure object
        ax: matplotlib axes object
        plotting_mode (str): 'single' or 'multi'
        energies (np.array): Energy values (for single mode)
        dos_values (np.array): DOS values (for single mode)
        multi_file_data (list): Multi-file data (for multi mode)
        energy_min (float): Minimum energy for plotting
        energy_max (float): Maximum energy for plotting
        line_color (str): Color for the DOS line
        line_width (float): Width of the DOS line
        show_fermi (bool): Whether to show Fermi level
        fermi_color (str): Color for Fermi level line
        show_grid (bool): Whether to show grid
        grid_alpha (float): Grid transparency
        font_size (int): Font size for labels
        title_font_size (int): Font size for title
        color_scheme (str): Color scheme for multiple files
    
    Returns:
        str: Plot title
    """
    if plotting_mode == "single":
        # Single file plot
        mask = (energies >= energy_min) & (energies <= energy_max)
        filtered_energies = energies[mask]
        filtered_dos = dos_values[mask]
        
        ax.plot(filtered_energies, filtered_dos, 
               color=line_color,
               linewidth=line_width,
               label='Total DOS')
        
        plot_title = 'VASP Density of States'
        
    else:  # multi-file mode
        # Multi-file plot
        colors = generate_colors(len(multi_file_data), color_scheme)
        
        for i, (file_energies, file_dos_values, file_path) in enumerate(multi_file_data):
            mask = (file_energies >= energy_min) & (file_energies <= energy_max)
            filtered_energies = file_energies[mask]
            filtered_dos = file_dos_values[mask]
            
            if len(filtered_energies) > 0:
                legend_label = format_legend_label(file_path)
                ax.plot(filtered_energies, filtered_dos, 
                       color=colors[i],
                       linewidth=line_width,
                       label=legend_label)
        
        plot_title = 'Multi-File DOS Comparison'
    
    # Add Fermi level if enabled
    if show_fermi:
        ax.axvline(x=0, color=fermi_color, 
                  linestyle='--', alpha=0.7, linewidth=2, 
                  label='Fermi Level')
    
    # Customize plot
    ax.set_xlabel('Energy (eV)', fontsize=font_size)
    ax.set_ylabel('Density of States (states/eV)', fontsize=font_size)
    ax.set_title(plot_title, fontsize=title_font_size, fontweight='bold')
    
    if show_grid:
        ax.grid(True, alpha=grid_alpha)
    
    ax.legend()
    ax.set_xlim(energy_min, energy_max)
    
    return plot_title

if __name__ == "__main__":
    print("Real VASP DOS Plotting Script")
    print("=" * 40)
    
    try:
        # Read the real DOS data
        energies, dos_values = read_dos_file("RES/DOS0")
        
        print(f"Loaded {len(energies)} data points")
        print(f"Full energy range: {energies.min():.3f} to {energies.max():.3f} eV")
        
        # Plot with -7 to 7 eV bounds as requested
        plot_dos_real(energies, dos_values, energy_range=(-7, 7))
        
        # Save filtered data
        save_filtered_data(energies, dos_values, energy_range=(-7, 7))
        
    except FileNotFoundError:
        print("Error: RES/DOS0 file not found!")
        print("Please make sure the DOS file is in the RES/ directory")
    except Exception as e:
        print(f"Error: {e}")

#!/usr/bin/env python3
"""
Plot real DOS data from VASP RES/DOS0 file
"""

import numpy as np
import matplotlib.pyplot as plt
import os

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

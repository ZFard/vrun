#!/usr/bin/env python3
"""
Example script demonstrating VASP DOS Plotter CLI usage
This script shows how to use the CLI programmatically
"""

import subprocess
import os
import numpy as np

def create_sample_dos_data():
    """Create sample DOS data for demonstration"""
    print("Creating sample DOS data...")
    
    # Create sample data 1: Clean surface
    energies1 = np.linspace(-10, 10, 200)
    dos1 = np.exp(-(energies1 + 3)**2/2) + 0.5*np.exp(-(energies1 - 2)**2/1.5)
    
    with open('clean_dos.txt', 'w') as f:
        f.write("# Energy Total_DOS Spin_Up Spin_Down\n")
        for e, d in zip(energies1, dos1):
            f.write(f"{e:.6f} {d:.6f} {d/2:.6f} {d/2:.6f}\n")
    
    # Create sample data 2: H-bridge
    dos2 = 0.8*np.exp(-(energies1 + 1)**2/1.5) + 0.6*np.exp(-(energies1 - 3)**2/2)
    
    with open('h_bridge_dos.txt', 'w') as f:
        f.write("# Energy Total_DOS Spin_Up Spin_Down\n")
        for e, d in zip(energies1, dos2):
            f.write(f"{e:.6f} {d:.6f} {d/2:.6f} {d/2:.6f}\n")
    
    # Create sample data 3: O-vacancy
    dos3 = 1.2*np.exp(-(energies1 + 2)**2/1.8) + 0.4*np.exp(-(energies1 - 1)**2/1.2)
    
    with open('o_vacancy_dos.txt', 'w') as f:
        f.write("# Energy Total_DOS Spin_Up Spin_Down\n")
        for e, d in zip(energies1, dos3):
            f.write(f"{e:.6f} {d:.6f} {d/2:.6f} {d/2:.6f}\n")
    
    print("✓ Sample data created: clean_dos.txt, h_bridge_dos.txt, o_vacancy_dos.txt")

def run_cli_command(cmd, description):
    """Run a CLI command and display results"""
    print(f"\n{description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print("✓ Command completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Command failed with return code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    """Main demonstration function"""
    print("VASP DOS Plotter CLI Usage Examples")
    print("=" * 50)
    
    # Create sample data
    create_sample_dos_data()
    
    # Example 1: Quick plot (using plotter directly)
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "quick", "clean_dos.txt", "-o", "example1_quick.png"],
        "Example 1: Quick plot with default settings"
    )
    
    # Example 2: Single file with custom settings
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "plot", "single", "clean_dos.txt", 
         "-r", "-5", "5", "-o", "example2_custom.png", 
         "--color", "red", "--width", "3", "--dpi", "300"],
        "Example 2: Single file with custom settings"
    )
    
    # Example 3: Multi-file comparison
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "plot", "multi", 
         "clean_dos.txt", "h_bridge_dos.txt", "o_vacancy_dos.txt",
         "-r", "-6", "6", "-o", "example3_comparison.png",
         "-c", "rainbow", "--width", "2.5"],
        "Example 3: Multi-file comparison plot"
    )
    
    # Example 4: High-resolution publication plot
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "plot", "single", "clean_dos.txt",
         "-r", "-4", "4", "-o", "example4_publication.pdf",
         "--color", "black", "--width", "2", "--dpi", "600", "--size", "10", "6"],
        "Example 4: High-resolution publication plot"
    )
    
    # Example 5: Batch processing
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "plot", "multi", "*.txt",
         "-r", "-8", "8", "-o", "example5_batch.png", "-c", "viridis"],
        "Example 5: Batch processing with wildcards"
    )
    
    # Display help
    print("\n" + "=" * 50)
    print("CLI Help System")
    print("=" * 50)
    run_cli_command(
        ["python", "vasp_dos_plotter/plotter.py", "--help"],
        "General help"
    )
    
    # Clean up
    print("\nCleaning up example files...")
    files_to_remove = [
        'clean_dos.txt', 'h_bridge_dos.txt', 'o_vacancy_dos.txt',
        'example1_quick.png', 'example2_custom.png', 'example3_comparison.png',
        'example4_publication.pdf', 'example5_batch.png'
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"✓ Removed {file}")
    
    print("\n" + "=" * 50)
    print("CLI Examples Complete!")
    print("=" * 50)
    print("For more information, see:")
    print("- CLI_USAGE_GUIDE.md (comprehensive guide)")
    print("- CLI_QUICK_REFERENCE.md (quick reference)")
    print("- python vasp_dos_cli.py --help (command help)")

if __name__ == "__main__":
    main()

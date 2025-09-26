# VASP DOS Plotter GUI - Usage Guide

## 🚀 **Advanced Features for Professional DOS Analysis**

### **Real-time Updates**
- ✅ **Automatic Plot Updates**: Changes to settings now update the plot automatically
- ✅ **Debounced Updates**: Prevents excessive redrawing while you're typing
- ✅ **Input Validation**: Real-time validation of energy range inputs
- ✅ **Progress Indicators**: Visual feedback on all operations

### **🎯 Interactive Sliders**
- ✅ **Fun Range Adjustment**: Drag sliders for smooth, interactive energy range control
- ✅ **Real-time Feedback**: See plot updates as you drag the sliders
- ✅ **Smart Validation**: Sliders automatically prevent min > max conflicts
- ✅ **Dynamic Ranges**: Slider ranges adjust based on your data
- ✅ **Visual Feedback**: Live display of current range values
- ✅ **Context-Aware**: Sliders adapt to single-file vs multi-file plotting modes

### **🔄 Multi-File Plotting**
- ✅ **Comparative Analysis**: Plot multiple DOS files together in a single plot
- ✅ **Color Differentiation**: Each file gets a unique color from selectable schemes
- ✅ **Smart Legend**: File paths shown with intelligent truncation and formatting
- ✅ **Context-Aware Settings**: All controls adapt to multi-file mode
- ✅ **Threaded Processing**: Non-blocking file loading for multiple files

### **Enhanced Responsiveness**
- ✅ **Threaded File Loading**: Large files load without freezing the interface
- ✅ **Error Handling**: Graceful handling of invalid inputs and file errors
- ✅ **Status Updates**: Clear feedback on what the application is doing
- ✅ **Non-blocking Operations**: UI remains responsive during all operations

## 📋 **How to Use the Improved GUI**

### **1. Loading Data**
- **Browse**: Click "Browse" to select any DOS file (defaults to "All files")
- **Sample Data**: Click "Load Sample" for demonstration (automatically loads on startup)
- **Progress**: Watch the progress indicator during loading
- **Tabbed Interface**: Switch between "Single File" and "Multi-File Plot" tabs

### **2. Energy Range Settings**
- **Text Entry**: Type in the energy range fields and see updates automatically
- **Interactive Sliders**: 🎯 **NEW!** Drag sliders for fun, real-time range adjustment
- **Validation**: Invalid inputs are caught and displayed
- **Auto-detect**: Click "Auto-detect Range" for optimal bounds
- **Zoom to Data**: Use "Zoom to Data" to see the full range
- **Reset to -7,7**: Quick reset to your default range

### **3. Appearance Customization**
- **Live Preview**: All changes update the plot immediately
- **Line Settings**: Adjust width and color with real-time feedback
- **Grid Options**: Toggle grid and adjust transparency
- **Font Control**: Change font sizes and see results instantly

### **4. Multi-File Plotting** 🔄
- **Add Files**: Click "Add Files" to select multiple DOS files for comparison
- **File Management**: Use "Clear List" or "Remove Selected" to manage your file list
- **Color Schemes**: Choose from auto, rainbow, viridis, plasma, or tab10 color palettes
- **Plot All Together**: Create a single plot with all selected files
- **Smart Legend**: Each file appears with its path (intelligently truncated)
- **Clear Plot**: Reset to empty plot state
- **Save Multi-Plot**: Export the combined visualization

### **5. Plot Controls**
- **Update Plot**: Manual refresh if needed
- **Reset View**: Return to auto-detected settings
- **Zoom to Data**: Show full data range (context-aware for current mode)
- **Progress Indicator**: Shows current operation status

### **6. Export Options**
- **Multiple Formats**: PNG, PDF, SVG support
- **High Resolution**: Adjustable DPI up to 600
- **Custom Sizing**: Set figure dimensions
- **Data Export**: Save filtered data as CSV

## 🎯 **Context-Aware Features**

### **Smart Mode Detection**
- **Single File Mode**: Automatically activated when loading individual files
- **Multi-File Mode**: Automatically activated when creating multi-file plots
- **Mode Indicators**: Slider info shows "Single file Range" vs "Multi-file Range"
- **Adaptive Controls**: All settings adapt to the current plotting mode

### **Intelligent Auto-Detection**
- **Single File**: Uses data from the loaded file for range detection
- **Multi-File**: Uses combined data from all selected files for optimal range
- **Context Messages**: Shows "Single file auto-detected" vs "Multi-file auto-detected"

### **Smart Legend Formatting**
- **Path Display**: Shows file paths instead of just filenames
- **Directory Removal**: Removes current working directory when possible
- **Intelligent Truncation**: Truncates long paths with ellipsis (...)
- **Maximum Length**: Limits legend labels to 50 characters for readability

## 🔧 **Troubleshooting**

### **Common Issues and Solutions**

#### **"Invalid input" Error**
- **Cause**: Non-numeric values in energy range fields
- **Solution**: Enter valid numbers (e.g., -7.0, 7.0)

#### **"Min must be < Max" Error**
- **Cause**: Minimum energy is greater than maximum
- **Solution**: Ensure min value is less than max value

#### **"No data in range" Message**
- **Cause**: Energy range doesn't contain any data points
- **Solution**: Use "Auto-detect Range" or "Zoom to Data"

#### **"Loading file..." Stuck**
- **Cause**: Large file or file access issues
- **Solution**: Wait for completion or check file permissions

#### **Plot Not Updating**
- **Cause**: Invalid settings or data issues
- **Solution**: Check progress indicator for error messages

## 💡 **Tips for Best Results**

### **Energy Range**
- **Start with "Auto-detect Range"** for optimal view
- **Use the sliders** for fun, interactive range adjustment
- **Type in text fields** for precise values
- **Use -7 to 7 eV** for your specific requirements
- **Drag sliders smoothly** to see real-time plot updates

### **Performance**
- Large files (>10,000 points) may take a moment to load
- Real-time updates are debounced for smooth performance
- Use "Update Plot" button if automatic updates seem slow

### **Export Quality**
- Use DPI 300+ for publication-quality plots
- PNG format is best for most applications
- PDF format preserves vector graphics

### **File Formats**
- Supports standard VASP DOS format
- Handles files with comment lines (starting with #)
- Works with tab or space-separated data

## 🎯 **Quick Start Checklist**

1. ✅ **Launch GUI**: `python run_gui.py`
2. ✅ **Load Data**: Click "Load Sample" or browse for your file
3. ✅ **Set Range**: Use -7 to 7 eV or click "Auto-detect Range"
4. ✅ **Customize**: Adjust colors, fonts, and appearance as needed
5. ✅ **Export**: Save your plot in desired format

## 📊 **Status Indicators**

- **"Ready"**: All operations complete, ready for input
- **"Loading file..."**: File is being read
- **"Updating plot..."**: Plot is being redrawn
- **"Invalid input"**: Check your energy range values
- **"No data in range"**: Adjust energy range
- **"Error: [message]"**: Specific error occurred

The improved GUI now provides a much more responsive and user-friendly experience with real-time feedback and better error handling!

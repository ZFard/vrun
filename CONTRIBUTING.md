# Contributing to VASP DOS Plotter

Thank you for your interest in contributing to the VASP DOS Plotter! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of VASP and Density of States calculations

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/vasp-dos-plotter.git
   cd vasp-dos-plotter
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Test the installation**:
   ```bash
   python dos_plotter_gui.py
   ```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Project Structure

```
vasp-dos-plotter/
├── dos_plotter_gui.py      # Main GUI application
├── plot_real_dos.py        # Command-line plotting script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # This file
├── .gitignore            # Git ignore rules
├── .gitattributes        # Git attributes
├── logo.png              # Application logo
├── icon.png              # Application icon
├── favicon.png           # Web favicon
├── DrZ.png               # Author photo/mascot
└── RES/                  # Sample data
    └── DOS0              # Sample DOS file
```

### Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding guidelines

3. **Test your changes**:
   - Test with different DOS file formats
   - Verify GUI responsiveness
   - Check error handling

4. **Update documentation** if needed:
   - Update README.md for new features
   - Add usage examples
   - Update GUI_USAGE_GUIDE.md

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment information**:
   - Operating system and version
   - Python version
   - Package versions (from `pip list`)

2. **Steps to reproduce**:
   - Clear, numbered steps
   - Sample data files if applicable

3. **Expected vs actual behavior**:
   - What you expected to happen
   - What actually happened

4. **Error messages**:
   - Full error traceback
   - Screenshots if relevant

## 💡 Feature Requests

When requesting features, please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and why it would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and alternatives

## 📝 Pull Request Guidelines

### Before Submitting

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings
- [ ] Code is tested and working
- [ ] Documentation is updated
- [ ] No merge conflicts with main branch

### PR Description

Include:
- **Summary** of changes
- **Motivation** for the changes
- **Testing** performed
- **Screenshots** for GUI changes
- **Breaking changes** if any

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different systems
4. **Documentation review**

## 🧪 Testing

### Manual Testing

- Test with various DOS file formats
- Verify GUI responsiveness
- Check error handling with invalid files
- Test on different operating systems

### Test Data

- Use the provided sample data in `RES/`
- Create test cases for edge cases
- Verify backward compatibility

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions
- Include type hints where appropriate
- Comment complex algorithms

### User Documentation

- Update README.md for new features
- Add examples and use cases
- Update GUI_USAGE_GUIDE.md for UI changes

## 🏷️ Release Process

Releases are managed by maintainers:

1. **Version bumping** in code
2. **Changelog updates**
3. **Git tag creation**
4. **GitHub release creation**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: Contact maintainers for sensitive issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to the VASP DOS Plotter! 🎉

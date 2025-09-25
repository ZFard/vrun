# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in the VASP DOS Plotter, please report it to us as described below.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: [zfard@iastate.edu](mailto:zfard@iastate.edu)

### What to Include

When reporting a vulnerability, please include:

1. **Description**: A clear description of the vulnerability
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Impact**: The potential impact of the vulnerability
4. **Environment**: Your operating system, Python version, and package versions
5. **Proof of Concept**: If possible, provide a minimal example that demonstrates the issue

### Response Timeline

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 1 week
- **Resolution**: We will work to resolve the issue as quickly as possible, typically within 30 days

### What to Expect

- We will keep you informed of our progress
- We will credit you in our security advisories (unless you prefer to remain anonymous)
- We will work with you to ensure the vulnerability is properly addressed

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**: Regularly update your Python packages
2. **Use Virtual Environments**: Always use virtual environments to isolate dependencies
3. **Validate Input Files**: Only use trusted DOS files from reliable sources
4. **Review Code**: If using the source code, review it before execution

### For Developers

1. **Input Validation**: Always validate user input and file contents
2. **Error Handling**: Implement proper error handling to avoid information disclosure
3. **Dependencies**: Keep dependencies updated and review security advisories
4. **Code Review**: All code changes should be reviewed for security implications

## Known Security Considerations

### File Handling
- The application reads DOS files from the filesystem
- Always validate file contents before processing
- Be cautious with files from untrusted sources

### GUI Security
- The application uses tkinter for the GUI
- No network communication is performed
- All processing is done locally

### Dependencies
- We use well-maintained scientific Python packages
- Dependencies are regularly updated
- Security advisories are monitored

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) and will be clearly marked in the changelog.

## Contact

For security-related questions or concerns, please contact:
- **Email**: [zfard@iastate.edu](mailto:zfard@iastate.edu)
- **GitHub**: [@zeinabfard](https://github.com/zeinabfard)

## Acknowledgments

We thank the security researchers and community members who help us keep the VASP DOS Plotter secure.

# Recruitment Application

## Overview
This project is a cross-platform recruitment application built using Python 3.11.4 and the [Flet](https://flet.dev) framework. While the application is optimized for Windows 11, it also supports Linux and macOS. Its primary purpose is to assist recruitment agencies in collecting candidate resumes based on specific filters, extracting their complete information and contact details, and saving the data to an Excel file.

Developed entirely from scratch by [Ambassador-of-programming](https://github.com/Ambassador-of-programming).

---

## Features
- Cross-platform compatibility (Windows, Linux, macOS).
- Candidate resume filtering based on user-defined criteria.
- Data extraction including full candidate details and contact information.
- Saves collected data to an Excel file for easy access and sharing.
- Built with the Flet library for a modern and interactive user interface.

---

## Prerequisites
### Python Version
Ensure that Python 3.11.4 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Virtual Environment
This project uses `pipenv` for managing dependencies and virtual environments.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ambassador-of-programming/FletHResumeTool
   cd https://github.com/Ambassador-of-programming/FletHResumeTool
   ```

2. Install `pipenv` if it is not already installed:
   ```bash
   pip install pipenv
   ```

3. Set up the virtual environment and install dependencies:
   ```bash
   pipenv install
   ```

4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

---

## Dependencies
The project relies on the following Python libraries:

- **undetected-chromedriver**: For bypassing detection when interacting with web browsers.
- **beautifulsoup4**: For parsing and scraping HTML content.
- **pandas**: For data manipulation and analysis.
- **openpyxl**: For working with Excel files.
- **numpy**: For numerical computations.
- **nuitka**: For compiling Python scripts into standalone executables.
- **imageio**: For handling image input and output.
- **cryptography**: For secure data encryption and decryption.
- **fake-useragent**: For generating random user-agent strings.
- **flet**: For building the cross-platform graphical user interface.

---

## Usage
1. Launch the application:
   ```bash
   python main.py
   ```

2. Define the filters for resume collection using the application interface.

3. Collect candidate data and export it to an Excel file.

4. Locate the Excel file in the output directory.

---

## Build Instructions
To create a standalone executable, use `Nuitka`:
1. Ensure Nuitka is installed in your environment:
   ```bash
   pipenv install nuitka
   ```

2. Build the executable:
   ```bash
   nuitka --onefile --windows-console-mode=disable --windows-icon-from-ico=icon.png main.py
   ```

---

## Acknowledgments
Special thanks to the developers of the libraries used in this project:
- [Flet](https://flet.dev)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- [Nuitka](https://nuitka.net/)

For more details, please refer to the official documentation of each library.


# HaFMaining

HaFMaining is a tool for extracting required information from `.txt` files exported from Jablotron F-Link.

---

## Features

- **Import F-Link TXT files**: Load configuration data exported from F-Link.
- **Automatic Extraction**: Parses and extracts `Type`, `HW`, and `FW` for the central unit and all connected devices.
- **User-Friendly GUI**: Simple interface for file selection and data viewing.
- **Export**: Supports exporting results to `.txt`, `.xlsx`, and `.json` formats.
- **API Key Generator**: Easily generate and copy an API key for integration with other applications.

---

## Installation

Currently, run directly from the command line:

1. **Install dependencies:**
    ```bash
    pip install openpyxl
    ```
2. **Download or clone this repository.**

---

## Usage

- **Run the application:**
    ```bash
    python infoMain.py
    ```
    or use the generated `.exe` if you have built it with PyInstaller.

- **Workflow:**
    1. Open the app (`infoMain.py` or `.exe`)
    2. Select your exported F-Link `.txt` file
    3. View extracted data (`Type`, `HW`, `FW`)
    4. Export results to `.txt`, `.xlsx`, or `.json` as needed

---

## Example

```python
# Launch HaFMaining
python infoMain.py

# Select F-Link TXT file
# Data is extracted and displayed in the app

# Export to your preferred format via the GUI



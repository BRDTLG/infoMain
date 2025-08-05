# F-Link TXT Analyzer – Technical Notes

## Overview

This Python Tkinter application enables the user to import, parse, and export configuration data from F-Link TXT files (Jablotron central and device lists).  
It is designed to be simple to use, portable, and extendable for future needs.

---

## Features

- **TXT Import**  
  Imports configuration data from F-Link exported TXT files.  
  Extracts data for one central (Type, HW, FW) and a list of devices (ID, Type, HW, FW).

- **Table Display**  
  Device list is displayed in a sortable table using Tkinter's `ttk.Treeview`.

- **Exports**  
  Supports data export to:
    - Plain TXT file (human-readable)
    - XLSX file (Excel, via openpyxl)
    - JSON file (machine-readable structure)

- **API Key Generator**  
  Random API key generation (letters + digits), with copy-to-clipboard function for easy integration with web or REST API use cases.

---

## Code Structure

- **parse_txt(file_path)**  
  Parses the TXT file using regular expressions. Returns two Python data structures: one dict for the central unit, and a list of dicts for devices.

- **GUI Design**  
  Built using standard Tkinter + ttk.  
  Controls are arranged in a single main window for usability and clarity.

- **Export Functions**  
  - TXT: Writes human-friendly summary.
  - XLSX: Uses openpyxl for robust Excel compatibility.
  - JSON: Uses Python’s `json` library with UTF-8 encoding and pretty formatting.

- **State Management**  
  All loaded data is held in the global variable `current_data`, allowing all event handlers access.

- **API Key Pop-up**  
  Opens a child window to display and copy a newly generated API key.

---

## Installation & Requirements

- **Python Version:**  
  Python 3.7+ recommended.

- **Dependencies:**  
  - `openpyxl` (for XLSX export)  
    Install via: `pip install openpyxl`
  - No other external libraries required – all other code relies on Python’s standard library.

- **Windows EXE packaging:**  
  Use PyInstaller for single-file distribution:  
  `pyinstaller --onefile main.py`

---

## Limitations

- **Central Parsing:**  
  Only the first detected central (JA-103K or JA-107K) is parsed; multiple centrals in one file are not supported.
- **Device Parsing:**  
  Only device blocks starting with an integer (e.g., `1:`, `2:`) are parsed.  
  Special Section blocks or different TXT layouts may require adjustments to the regex.
- **TXT Format:**  
  Input TXT must be in the structure exported from F-Link (tested on provided examples).
- **No Editing:**  
  This version does not allow direct editing of the data within the GUI.

---

## Security Notes

- **API Key**:  
  The generated API key is random and not stored persistently. For actual production use, always use secure random sources and, if possible, manage keys outside of the application (environment variables, vaults, etc.).
- **Input Validation:**  
  Minimal input validation is performed.  
  For more robust use (especially if data is processed from untrusted sources), additional validation and error handling should be implemented.

---

## Extensions & Integrations

- **Additional Exports:**  
  CSV, XML, or direct API calls can be added as needed.
- **Multiple Central Units:**  
  With minimal changes to the regex, support for multiple centrals could be implemented.
- **Direct Web Integration:**  
  The API key feature enables easy copy-paste integration with web frontends or REST API clients.

---

## Troubleshooting

- **openpyxl Not Installed:**  
  XLSX export will fail unless openpyxl is installed (`pip install openpyxl`).
- **Tkinter Issues:**  
  Tkinter is standard in most Python distributions. On Linux, it may require installing an additional package (`sudo apt install python3-tk`).
- **Character Encoding:**  
  The app uses UTF-8 throughout. Ensure your TXT files are in UTF-8 for best compatibility.

---

## Authors & License

- Written by: [your name/team/company here]
- License: [choose appropriate license, e.g., MIT]

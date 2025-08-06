import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os
import random
import string
import openpyxl
import json

def parse_txt(file_path):
    """
    Parses the given TXT file for central and device information.
    Returns:
        central (dict): Info about the central unit (Type, FW, HW).
        devices (list of dict): List of devices with ID, Type, FW, HW.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex: Find central info (Type, FW, HW) – only first match is used
    central_pattern = r'Type:\s*(JA-103K|JA-107K).*?FW:\s*([\w\.-]+).*?HW:\s*([\w\.-]+)'
    central_match = re.search(central_pattern, text, re.DOTALL)
    if central_match:
        central = {
            'Type': central_match.group(1),
            'FW': central_match.group(2),
            'HW': central_match.group(3)
        }
    else:
        central = {'Type': '', 'FW': '', 'HW': ''}

    # Regex: Find all device blocks with ID, Type, FW, HW
    device_pattern = r'(\d+):\n\s*Type:\s*([\w\-]+).*?FW:\s*([\w\.\-]+).*?HW:\s*([\w\.\-]+)'
    devices = []
    for match in re.finditer(device_pattern, text, re.DOTALL):
        devices.append({
            'ID': match.group(1),
            'Type': match.group(2),
            'FW': match.group(3),
            'HW': match.group(4)
        })
    return central, devices

def load_file():
    """
    Opens a file dialog for the user to select a TXT file.
    Parses the file and updates the GUI.
    """
    file_path = filedialog.askopenfilename(title="Select TXT file", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    global current_data
    current_data['central'], current_data['devices'] = parse_txt(file_path)
    current_data['file_path'] = file_path
    update_view()

def update_view():
    """
    Updates the GUI display with current data (central, devices).
    """
    c = current_data['central']
    central_str = f"{c['Type']}, HW: {c['HW']}, FW: {c['FW']}"
    central_var.set(central_str)
    # Clear and refill the table
    for row in table.get_children():
        table.delete(row)
    for d in current_data['devices']:
        table.insert('', 'end', values=(d['ID'], d['Type'], d['FW'], d['HW']))

def export_txt():
    """
    Exports currently displayed data to a plain TXT file.
    """
    if not current_data['devices'] or not current_data['central']['Type']:
        messagebox.showinfo("Export", "No data loaded.")
        return
    file_path = filedialog.asksaveasfilename(
        title="Export to TXT",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not file_path:
        return
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Central:\n")
            c = current_data['central']
            f.write(f"Type: {c['Type']}\nHW: {c['HW']}\nFW: {c['FW']}\n\n")
            f.write("Devices:\n")
            for d in current_data['devices']:
                f.write(f"{d['ID']}: Type: {d['Type']}, HW: {d['HW']}, FW: {d['FW']}\n")
        messagebox.showinfo("Export", f"Data successfully exported to:\n{os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Export error", str(e))

def export_xlsx():
    """
    Exports currently displayed data to an Excel .xlsx file.
    Requires openpyxl.
    """
    if not current_data['devices'] or not current_data['central']['Type']:
        messagebox.showinfo("Export", "No data loaded.")
        return
    file_path = filedialog.asksaveasfilename(
        title="Export to XLSX",
        defaultextension=".xlsx",
        filetypes=[("Excel file", "*.xlsx")]
    )
    if not file_path:
        return
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "F-Link Data"
        # Central info in first rows
        c = current_data['central']
        ws.append(["Central"])
        ws.append(["Type", "HW", "FW"])
        ws.append([c['Type'], c['HW'], c['FW']])
        ws.append([])
        # Devices
        ws.append(["Devices"])
        ws.append(["ID", "Type", "FW", "HW"])
        for d in current_data['devices']:
            ws.append([d['ID'], d['Type'], d['FW'], d['HW']])
        wb.save(file_path)
        messagebox.showinfo("Export", f"Data successfully exported to:\n{os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Export error", str(e))

def export_json():
    """
    Exports currently displayed data to a JSON file.
    Data structure:
    {
        "central": {...},
        "devices": [...]
    }
    """
    if not current_data['devices'] or not current_data['central']['Type']:
        messagebox.showinfo("Export", "No data loaded.")
        return
    file_path = filedialog.asksaveasfilename(
        title="Export to JSON",
        defaultextension=".json",
        filetypes=[("JSON file", "*.json")]
    )
    if not file_path:
        return
    try:
        data = {
            "central": current_data['central'],
            "devices": current_data['devices']
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Export", f"Data successfully exported to:\n{os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Export error", str(e))

def clear_all():
    """
    Clears all currently displayed and loaded data from the GUI.
    """
    current_data['central'] = {'Type': '', 'FW': '', 'HW': ''}
    current_data['devices'] = []
    current_data['file_path'] = None
    central_var.set("")
    for row in table.get_children():
        table.delete(row)

def generate_api_key(length=32):
    """
    Generates a random API key (letters and digits).
    Args:
        length (int): Desired key length.
    Returns:
        str: API key.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def show_api_key():
    """
    Displays a generated API key in a pop-up dialog with a copy-to-clipboard option.
    """
    api_key = generate_api_key()
    # Function to copy the key to clipboard
    def copy_key():
        root.clipboard_clear()
        root.clipboard_append(api_key)
        msg_label.config(text="Copied to clipboard!")
    api_win = tk.Toplevel(root)
    api_win.title("API Key for Web App Import")
    api_win.geometry("420x120")
    lbl = tk.Label(api_win, text="Your API Key:", font=("Arial", 11))
    lbl.pack(pady=(12, 3))
    entry = tk.Entry(api_win, font=("Arial", 11), width=40, justify='center')
    entry.pack()
    entry.insert(0, api_key)
    entry.config(state='readonly')
    btn = tk.Button(api_win, text="Copy", command=copy_key)
    btn.pack(pady=(7, 0))
    msg_label = tk.Label(api_win, text="", fg="green", font=("Arial", 9))
    msg_label.pack()
    api_win.transient(root)
    api_win.grab_set()
    api_win.mainloop()

# ---- DATA HOLDER ----
current_data = {
    'central': {'Type': '', 'FW': '', 'HW': ''},
    'devices': [],
    'file_path': None
}

# ---- GUI SETUP ----
root = tk.Tk()
root.title("F-Link TXT Analyzer TLG")
root.geometry("750x430")

# --- Top controls: Load, Clear, Export, API key ---
frm_top = tk.Frame(root)
frm_top.pack(padx=10, pady=10, fill='x')

btn_load = tk.Button(frm_top, text="Select TXT file", command=load_file)
btn_load.pack(side='left')

btn_clear = tk.Button(frm_top, text="New file", command=clear_all)
btn_clear.pack(side='left', padx=(8,0))

btn_export_txt = tk.Button(frm_top, text="Export to TXT", command=export_txt)
btn_export_txt.pack(side='left', padx=(8,0))

btn_export_xlsx = tk.Button(frm_top, text="Export to XLSX", command=export_xlsx)
btn_export_xlsx.pack(side='left', padx=(8,0))

btn_export_json = tk.Button(frm_top, text="Export to JSON", command=export_json)
btn_export_json.pack(side='left', padx=(8,0))

btn_api = tk.Button(frm_top, text="API Key", command=show_api_key)
btn_api.pack(side='left', padx=(8,0))

# --- Central info display ---
central_var = tk.StringVar()
lbl_central = tk.Label(frm_top, textvariable=central_var, font=('Arial', 11, 'bold'), fg='darkblue')
lbl_central.pack(side='left', padx=16)

# --- Table for devices ---
frm_table = tk.Frame(root)
frm_table.pack(padx=10, pady=(0,10), fill='both', expand=True)

columns = ("ID", "Type", "FW", "HW")
table = ttk.Treeview(frm_table, columns=columns, show='headings', height=12)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=80 if col == "ID" else 110, anchor='w')
table.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(frm_table, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# --- Exit button ---
btn_exit = tk.Button(root, text="Exit", command=root.destroy)
btn_exit.pack(pady=8)

# --- Start the GUI event loop ---
root.mainloop()

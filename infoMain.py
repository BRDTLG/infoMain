import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Ústředna: hledáme pouze první výskyt
    central_pattern = r'Type:\s*(JA-103K|JA-107K).*?FW:\s*([\w\.-]+).*?HW:\s*([\w\.-]+)'
    central_match = re.search(central_pattern, text, re.DOTALL)
    central = {}
    if central_match:
        central = {
            'Type': central_match.group(1),
            'FW': central_match.group(2),
            'HW': central_match.group(3)
        }
    else:
        central = {'Type': '', 'FW': '', 'HW': ''}

    # Periferie: bloky začínající číslem
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
    file_path = filedialog.askopenfilename(title="Vyber TXT soubor", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    central, devices = parse_txt(file_path)
    # Zobraz ústřednu
    central_str = f"{central['Type']}, HW: {central['HW']}, FW: {central['FW']}"
    central_var.set(central_str)
    # Vymaž tabulku
    for row in table.get_children():
        table.delete(row)
    # Vyplň tabulku
    for d in devices:
        table.insert('', 'end', values=(d['ID'], d['Type'], d['FW'], d['HW']))

# --- GUI ---
root = tk.Tk()
root.title("Analýza F-Link TXT (Tkinter)")
root.geometry("550x380")

frm_top = tk.Frame(root)
frm_top.pack(padx=10, pady=10, fill='x')

btn_load = tk.Button(frm_top, text="Vybrat TXT soubor", command=load_file)
btn_load.pack(side='left')

central_var = tk.StringVar()
lbl_central = tk.Label(frm_top, textvariable=central_var, font=('Arial', 11, 'bold'), fg='darkblue')
lbl_central.pack(side='left', padx=16)

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

btn_exit = tk.Button(root, text="Ukončit", command=root.destroy)
btn_exit.pack(pady=8)

root.mainloop()

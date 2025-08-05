import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os

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
    global current_data
    current_data['central'], current_data['devices'] = parse_txt(file_path)
    current_data['file_path'] = file_path
    update_view()

def update_view():
    # Zobraz ústřednu
    c = current_data['central']
    central_str = f"{c['Type']}, HW: {c['HW']}, FW: {c['FW']}"
    central_var.set(central_str)
    # Vymaž tabulku
    for row in table.get_children():
        table.delete(row)
    # Vyplň tabulku
    for d in current_data['devices']:
        table.insert('', 'end', values=(d['ID'], d['Type'], d['FW'], d['HW']))

def export_txt():
    if not current_data['devices'] or not current_data['central']['Type']:
        messagebox.showinfo("Export", "Nejsou načtená žádná data.")
        return
    file_path = filedialog.asksaveasfilename(
        title="Exportovat do TXT",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if not file_path:
        return
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Ústředna:\n")
            c = current_data['central']
            f.write(f"Type: {c['Type']}\nHW: {c['HW']}\nFW: {c['FW']}\n\n")
            f.write("Periferie:\n")
            for d in current_data['devices']:
                f.write(f"{d['ID']}: Type: {d['Type']}, HW: {d['HW']}, FW: {d['FW']}\n")
        messagebox.showinfo("Export", f"Data byla úspěšně exportována do:\n{os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Chyba exportu", str(e))

def clear_all():
    current_data['central'] = {'Type': '', 'FW': '', 'HW': ''}
    current_data['devices'] = []
    current_data['file_path'] = None
    central_var.set("")
    for row in table.get_children():
        table.delete(row)

# --- Data holder ---
current_data = {
    'central': {'Type': '', 'FW': '', 'HW': ''},
    'devices': [],
    'file_path': None
}

# --- GUI ---
root = tk.Tk()
root.title("Analýza F-Link TXT (Tkinter)")
root.geometry("600x410")

frm_top = tk.Frame(root)
frm_top.pack(padx=10, pady=10, fill='x')

btn_load = tk.Button(frm_top, text="Vybrat TXT soubor", command=load_file)
btn_load.pack(side='left')

btn_clear = tk.Button(frm_top, text="Nový soubor", command=clear_all)
btn_clear.pack(side='left', padx=(8,0))

btn_export = tk.Button(frm_top, text="Exportovat do TXT", command=export_txt)
btn_export.pack(side='left', padx=(8,0))

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

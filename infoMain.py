import PySimpleGUI as sg
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

def make_table_data(devices):
    return [[d['ID'], d['Type'], d['FW'], d['HW']] for d in devices]

def main():
    sg.theme('LightBlue3')
    layout = [
        [sg.Text('Vyber TXT soubor:'), sg.InputText('', key='-FILE-', enable_events=True, visible=False), sg.FileBrowse('Vybrat soubor', file_types=(("Text Files", "*.txt"),))],
        [sg.Text('Ústředna:'), sg.Text('', key='-CENTRAL-')],
        [sg.Table(values=[], headings=['ID', 'Type', 'FW', 'HW'], auto_size_columns=True, key='-TABLE-', justification='left', num_rows=10)],
        [sg.Button('Ukončit')]
    ]
    window = sg.Window('Analýza F-Link TXT', layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Ukončit'):
            break
        if event == '-FILE-':
            file_path = values['-FILE-']
            if file_path:
                central, devices = parse_txt(file_path)
                # Zobrazit ústřednu
                ctext = f"{central['Type']}, HW: {central['HW']}, FW: {central['FW']}"
                window['-CENTRAL-'].update(ctext)
                # Tabulka periferií
                table_data = make_table_data(devices)
                window['-TABLE-'].update(values=table_data)
    window.close()

if __name__ == '__main__':
    main()

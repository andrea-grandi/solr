import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import requests
import subprocess
import platform
from urllib.parse import unquote

# Funzione per cercare documenti in Solr
def search_documents(event):
    query = query_entry.get()

    solr_url = 'http://localhost:8983/solr'  # URL di Solr
    solr_core = 'core'  # Nome del core di Solr

    # URL per la ricerca
    url = f'{solr_url}/{solr_core}/select'

    # Parametri della ricerca
    params = {
        'q': query,
        'rows': 10,
        'fl': 'id,path'  # Campi da includere nella risposta
    }

    # Esegui la richiesta HTTP
    response = requests.get(url, params=params)
    response_json = response.json()

    # Estrai i risultati dalla risposta JSON
    results = response_json['response']['docs']

    # Aggiorna la tabella dei risultati
    result_listbox.delete(*result_listbox.get_children())
    for result in results:
        title = os.path.basename(result['id'])  # Estrai solo il nome del file dall'ID
        path = result['id']  # Utilizza il campo 'id' come percorso del file completo
        result_listbox.insert('', 'end', values=(title, path))

def open_file(event):
    selection = result_listbox.selection()
    if selection:
        item = selection[0]
        path = result_listbox.item(item, 'values')[1]
        try:
            subprocess.run(['open', path], check=True)  # Try to open the file with the default application
        except subprocess.CalledProcessError:
            folder_path = os.path.dirname(unquote(path))  # Get the folder path containing the file
            try:
                if platform.system() == 'Darwin':
                    subprocess.run(['open', folder_path], check=True)  # Open the folder and highlight the file in Finder (macOS)
                elif platform.system() == 'Windows':
                    subprocess.run(['explorer', '/select,', os.path.normpath(folder_path)], check=True)  # Open the folder and select the file in File Explorer (Windows)
                elif platform.system() == 'Linux':
                    subprocess.run(['xdg-open', os.path.normpath(folder_path)], check=True)  # Open the folder in the default file manager (Linux)
            except FileNotFoundError:
                pass  # Ignore any exceptions if opening the folder fails

# Creazione dell'interfaccia grafica
window = tk.Tk()
window.title('Solr Document Search')

# Apply a themed style to the window
style = ThemedStyle(window)
style.set_theme('arc')  # Choose the desired theme (e.g., 'arc', 'scidgrey', 'radiance', 'yaru')

# Aggiungi una tabella per i risultati
result_listbox = ttk.Treeview(window, columns=('ID', 'Path'))
result_listbox.heading('ID', text='Documenti')  # Modify the column heading
result_listbox.heading('Path', text='Percorso')  # Modify the column heading
result_listbox.grid(row=0, column=0, columnspan=2, sticky='nsew')

# Aggiungi un campo di testo per l'inserimento della query
query_entry = ttk.Entry(window)
query_entry.grid(row=1, column=0, padx=10, pady=5, sticky='we')
query_entry.focus()

# Aggiungi la gestione dell'evento di modifica del campo di ricerca
query_entry.bind('<KeyRelease>', search_documents)

# Aggiungi la gestione dell'evento di doppio clic per aprire il file
result_listbox.bind('<<TreeviewSelect>>', open_file)

# Configura il layout responsive
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=0)

window.mainloop()
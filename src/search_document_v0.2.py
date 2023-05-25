import tkinter as tk
import requests
import json
import subprocess

# Configurazione di Apache Solr
solr_url = 'http://localhost:8983/solr'  # URL di Solr
solr_core = 'test'  # Nome del core di Solr

# Funzione per eseguire la ricerca con Solr
def search_documents():
    query = entry.get()  # Ottieni il testo di ricerca dalla casella di input
    results = perform_solr_query(query)

    # Pulisci la lista dei risultati precedenti
    result_listbox.delete(0, tk.END)

    # Aggiungi i risultati alla lista
    for result in results:
        result_listbox.insert(tk.END, result['id'])

# Funzione per eseguire la query Solr
def perform_solr_query(query):
    # URL per l'esecuzione della query
    url = f'{solr_url}/{solr_core}/select'

    # Parametri della query
    params = {
        'q': query,
        'wt': 'json'
    }

    # Esegui la richiesta HTTP
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Estrai i risultati dalla risposta JSON
        data = json.loads(response.text)
        results = data['response']['docs']
        return results
    else:
        print(f"Errore durante l'esecuzione della query: {response.text}")
        return []

# Funzione per aprire il documento selezionato
def open_document(event):
    selected_document = result_listbox.get(result_listbox.curselection())
    subprocess.Popen(['open', selected_document])  # Modifica 'open' se stai usando un sistema operativo diverso da macOS

# Creazione della finestra dell'interfaccia grafica
window = tk.Tk()
window.title("Ricerca Documenti Solr")

# Creazione del campo di input per la ricerca
entry = tk.Entry(window)
entry.pack(pady=10)

# Creazione del pulsante di ricerca
search_button = tk.Button(window, text="Cerca", command=search_documents)
search_button.pack()

# Creazione della lista per i risultati
result_listbox = tk.Listbox(window)
result_listbox.pack(pady=10)

# Aggiungi il bind del doppio clic sulla lista per aprire il documento
result_listbox.bind('<Double-Button-1>', open_document)

# Avvio del loop di eventi dell'interfaccia grafica
window.mainloop()
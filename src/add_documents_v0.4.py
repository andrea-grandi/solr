import os
import time
import subprocess
import requests

# Configurazione Solr
solr_url = 'http://localhost:8983/solr'  # URL di base di Solr
solr_core = 'core'  # Nome del core di Solr

# Percorso alla directory di installazione di Solr
solr_home = '/Users/andreagrandi/Documents/solr-9.2.1'  # <--- Sostituisci con il tuo percorso corretto

# Cartella dei documenti da monitorare
document_folder = '/Users/andreagrandi/venvs/solr/doc'

# Lista dei documenti già indicizzati
indexed_documents = []

# Funzione per caricare i documenti in Solr
def load_documents(file_paths):
    for file_path in file_paths:
        # Esegue il comando bin/post di Solr per caricare il documento
        subprocess.run([os.path.join(solr_home, 'bin/post'), '-c', solr_core, file_path])
        print(f"Caricato documento: {file_path}")
        # Aggiungi il documento alla lista dei documenti indicizzati
        indexed_documents.append(file_path)

"""
# Funzione per eliminare un documento da Solr
def delete_document(doc_id):
    delete_url = f"{solr_url}/{solr_core}/update?commit=true"
    delete_data = f'<delete><query>id:"{doc_id}"</query></delete>'
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(delete_url, data=delete_data, headers=headers)
    if response.status_code == 200:
        print(f"Documento con ID {doc_id} eliminato da Solr")
        # Rimuovi il documento dalla lista dei documenti indicizzati
        indexed_documents.remove(doc_id)
    else:
        print(f"Errore durante l'eliminazione del documento con ID {doc_id} da Solr")
"""

# Funzione per eliminare un documento da Solr
def delete_document(doc_id):
    if doc_id in indexed_documents:
        delete_url = f"{solr_url}/{solr_core}/update?commit=true"
        delete_data = f'<delete><query>id:"{doc_id}"</query></delete>'
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(delete_url, data=delete_data, headers=headers)
        if response.status_code == 200:
            print(f"Documento con ID {doc_id} eliminato da Solr")
            # Rimuovi il documento dalla lista dei documenti indicizzati
            indexed_documents.remove(doc_id)
        else:
            print(f"Errore durante l'eliminazione del documento con ID {doc_id} da Solr")
    else:
        print(f"Il documento con ID {doc_id} non è presente nell'elenco dei documenti indicizzati")

# Loop principale
while True:
    # Ottiene l'elenco di tutti i file nella cartella e sottocartelle
    all_files = []
    for root, dirs, files in os.walk(document_folder):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    # Carica solo i documenti non ancora indicizzati
    files_to_index = [file_path for file_path in all_files if file_path not in indexed_documents]
    load_documents(files_to_index)

    # Ottiene l'elenco dei documenti indicizzati in Solr
    solr_query_url = f"{solr_url}/{solr_core}/select"
    solr_params = {'q': '*:*', 'fl': 'id', 'rows': 100000}
    response = requests.get(solr_query_url, params=solr_params)
    if response.status_code == 200:
        # Elenco dei documenti indicizzati in Solr
        solr_documents = response.json()['response']['docs']

        # Elenco dei file nella cartella document_folder
        files_in_folder = [f for f in all_files if os.path.isfile(f)]

        # Verifica se ci sono documenti indicizzati non presenti nella cartella
        documents_to_delete = []
        for doc in solr_documents:
            doc_id = doc['id']
            if doc_id not in files_in_folder:
                # Il documento non è presente nella cartella, quindi lo aggiungiamo alla lista dei documenti da eliminare
                documents_to_delete.append(doc_id)

        # Elimina i documenti indicizzati che non sono presenti nella cartella
        for doc_id in documents_to_delete:
            delete_document(doc_id)

    # Attendi un minuto prima di eseguire nuovamente il controllo
    time.sleep(60)




import requests
import os
import json

# Configurazione di Solr
solr_url = 'http://localhost:8983/solr'  # URL di Solr
solr_core = 'core_one'  # Nome del core di Solr

# Funzione per aggiungere documenti a Solr
def add_documents_to_solr(documents_path):
    # URL per l'aggiunta di documenti
    url = f'{solr_url}/{solr_core}/update'

    # Headers della richiesta HTTP
    headers = {
        'Content-Type': 'application/json'
    }

    # Lista dei documenti da inviare a Solr
    documents = []

    # Elabora i documenti nella cartella
    for root, dirs, files in os.walk(documents_path):
        for file in files:
            # Ottieni il percorso completo del documento
            document_path = os.path.join(root, file)

            # Crea un documento per Solr
            doc = {
                'id': document_path,  # Utilizza il percorso come ID univoco del documento
                'path': {'set': document_path},  # Aggiungi il percorso come campo 'path'
            }

            documents.append(doc)

    # Crea il payload per la richiesta
    payload = {
        'add': documents
    }

    # Converti il payload in formato JSON
    json_payload = json.dumps(payload)

    # Esegui la richiesta HTTP
    response = requests.post(url, headers=headers, data=json_payload)

    if response.status_code == 200:
        print('Documenti aggiunti con successo a Solr.')
    else:
        print(f"Errore durante l'aggiunta dei documenti: {response.text}")

# Esempio di utilizzo
documents_folder = '/Users/andreagrandi/Desktop/solr_tests'  # Sostituisci con il percorso della cartella dei documenti
add_documents_to_solr(documents_folder)
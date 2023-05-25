import os
import requests

# Configurazione di Apache Solr
solr_url = 'http://localhost:8983/solr'  # URL di Solr
solr_core = 'core_one'  # Nome del core di Solr

# Funzione per l'aggiunta di documenti a Solr
def add_documents_to_solr(folder_path):
    # Iterazione sui file presenti nella cartella
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Lettura del contenuto del file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        # Creazione del documento Solr
        document = {
            'id': filename,  # Utilizziamo il nome del file come ID del documento
            'content': content,  # Contenuto del documento
            'path': file_path # Percorso del file
        }

        # URL per l'aggiunta del documento
        url = f'{solr_url}/{solr_core}/update/json/docs'

        # Aggiunta del documento a Solr
        response = requests.post(url, json=document)

        if response.status_code == 200:
            print(f"Documento '{filename}' aggiunto con successo.")
        else:
            print(f"Errore durante l'aggiunta del documento '{filename}': {response.text}")

    # Commit delle modifiche
    commit_url = f'{solr_url}/{solr_core}/update?commit=true'
    requests.get(commit_url)

    print("Aggiunta dei documenti completata.")

# Esempio di utilizzo
folder_path = '/Users/andreagrandi/Desktop/solr_tests'  # Percorso della cartella contenente i documenti
add_documents_to_solr(folder_path)
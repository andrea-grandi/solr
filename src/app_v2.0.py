import subprocess

if __name__ == '__main__':
    add_script_path = '/Users/andreagrandi/venvs/solr/src/add_documents_v0.4.py'
    search_script_path = '/Users/andreagrandi/venvs/solr/src/webapp_search.py'

    # Esegui lo script add_documents_v0.4.py in un processo separato
    add_process = subprocess.Popen(['python3', add_script_path])

    # Esegui lo script search_documents_v0.4.py nel processo corrente
    subprocess.call(['python3', search_script_path])

    # Attendere il completamento del processo di add_documents_v0.4.py
    add_process.wait()

    # print("Esecuzione completata.")
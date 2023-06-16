import platform
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from datetime import timedelta
from flask import send_file, render_template
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'password'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # Imposta il tempo di scadenza a 1 minuto

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    # In una vera applicazione, questo metodo dovrebbe caricare l'utente dal sistema di autenticazione
    # Qui lo simuliamo creando un utente con il nome specificato
    return User(username)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Verify the user credentials
        if form.username.data == 'admin' and form.password.data == 'password':
            user = User(form.username.data)
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('search_documents'))  # Reindirizza a index.html dopo il login
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Pagina principale
@app.route('/')
def index():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')
    
def get_filename(path):
    return os.path.basename(path)
    
# Funzione per cercare documenti in Solr
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_documents():
    if request.method == 'POST':
        query = request.form.get('query', '')

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

        # Aggiorna i risultati con i nomi dei file e i percorsi relativi
        updated_results = []
        for result in results:
            filename = os.path.basename(result['id'])  # Estrai solo il nome del file dall'ID
            path = os.path.abspath(result['id'])  # Utilizza il percorso relativo al file
            updated_results.append({'filename': filename, 'path': path})

        return render_template('results.html', results=updated_results)
    else:
        return redirect(url_for('index'))

@app.route('/view_file', methods=['GET'])
@login_required
def view_file():
    path = request.args.get('path')
    try:
        return send_file(path, as_attachment=False)
    except FileNotFoundError:
        return render_template('exceptions.html', error_message='File not found: il file potrebbe essere stato eliminato dalla cartella ma non ancora da solr')

# Funzione per aprire un file
@app.route('/open_file', methods=['GET'])
@login_required
def open_file():
    path = request.args.get('path')
    return redirect(url_for('view_file', path=path))

app.jinja_env.globals.update(get_filename=get_filename)

if __name__ == '__main__':
    # Avvia l'app Flask
    app.run(debug=True)


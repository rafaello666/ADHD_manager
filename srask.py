from flask import Flask, session, render_template

app = Flask(__name__)

# Ustaw swój własny klucz – zastąp poniższy ciąg swoim kluczem
app.config['SECRET_KEY'] = 'chujwduperazdwatrzykindzeszczepanek'

@app.route('/')
def index():
    # Przykładowe użycie sesji
    session['wiadomosc'] = 'Witaj w aplikacji!'
    return f"Sesja: {session.get('wiadomosc')}"

if __name__ == '__main__':
    app.run(debug=True)

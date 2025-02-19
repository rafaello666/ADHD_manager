from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Pobierz token GitHub ze zmiennej środowiskowej
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Nie znaleziono tokenu GitHub. Ustaw zmienną środowiskową GITHUB_TOKEN.")

# Ustawienia repozytorium
OWNER = "Rafaello666"          # Twój login GitHub
REPO = "ADHD_manager"          # Nazwa repozytorium

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repo_contents(path=""):
    """
    Pobiera zawartość katalogu w repozytorium.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Błąd pobierania zawartości '{path}': {e}")
        return []

def process_file(file_item):
    """
    Pobiera zawartość pliku, wywołuje funkcję analizy oraz zapisuje wynik do pliku logu.
    """
    download_url = file_item.get("download_url")
    if download_url:
        try:
            file_content = requests.get(download_url).text
            analysis_result = analyze_code(file_content, file_item["path"])
            result_text = (
                f"Analiza pliku {file_item['path']}:\n"
                f"{analysis_result}\n{'-'*40}\n"
            )
            print(result_text)
            # Zapis wyniku do pliku 'analiza_log.txt'
            with open("analiza_log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(result_text)
        except Exception as e:
            print(f"Błąd przetwarzania pliku {file_item['path']}: {e}")

def traverse_repo(path=""):
    """
    Rekurencyjnie przegląda wszystkie katalogi repozytorium.
    """
    contents = get_repo_contents(path)
    for item in contents:
        if item["type"] == "file":
            process_file(item)
        elif item["type"] == "dir":
            traverse_repo(item["path"])

def analyze_code(code, file_path):
    """
    Funkcja wysyła kod do API modelu, które przeprowadza analizę.
    
    UWAGA:
    - Jeśli nie masz jeszcze działającego API, możesz tymczasowo zwracać przykładową analizę.
    - Jeśli masz już działające API, ustaw właściwy adres URL w model_api_url.
    """
    # Tymczasowe rozwiązanie – zwraca stałą odpowiedź:
    return "Przykładowa analiza: kod wygląda poprawnie, brak wykrytych błędów."

    # Jeśli masz działające API, zakomentuj powyższą linię i odkomentuj poniższy kod:
    """
    model_api_url = "https://moj-model-api.example.com/analyze"  # <-- Ustaw tutaj właściwy adres API
    prompt = (
        f"Przeanalizuj poniższy kod z pliku {file_path} i podaj wnioski dotyczące jego struktury, "
        f"potencjalnych błędów oraz sugestii usprawnień. Uwzględnij specyfikę narzędzia, które jest menadżerem życia "
        f"dla osoby z mocnym ADHD (użytkownik: Rafał Bartosik):\n\n{code}"
    )
    payload = {
        "prompt": prompt,
        "model": "o3-mini-high" 
        
    }
    try:
        response = requests.post(model_api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("analysis", "Brak analizy")
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas wywołania API dla pliku {file_path}: {e}")
        return "Błąd analizy"
    """

@app.route('/webhook', methods=['POST']) 
def webhook_handler():
    """
    Endpoint, który odbiera webhooki z GitHub.
    Po otrzymaniu powiadomienia (np. push event) przegląda repozytorium i analizuje pliki.
    """
    data = request.json
    print("Otrzymano webhook:", data.get("ref", "Brak informacji o gałęzi"))
    traverse_repo()
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    # Uruchomienie serwera na porcie 5000
    app.run(host="0.0.0.0", port=5000)

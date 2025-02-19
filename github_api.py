import requests

# Konfiguracja
GITHUB_TOKEN = "TWÓJ_TOKEN_GITHUB"
OWNER = "Rafaello666"
REPO = "ADHD_manager"

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repo_contents(path=""):
    """
    Pobiera zawartość katalogu w repozytorium.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def process_file(file_item):
    """
    Pobiera zawartość pliku i wywołuje funkcję analizy.
    """
    download_url = file_item.get("download_url")
    if download_url:
        file_content = requests.get(download_url).text
        analysis_result = analyze_code(file_content, file_item["path"])
        print(f"Analiza pliku {file_item['path']}:\n{analysis_result}\n{'-'*40}")

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
      - Przygotuj zapytanie (prompt) zawierające kod z pliku.
      - Wyślij zapytanie do API modelu (np. o3-mini-high).
      - Odbierz i zwróć wynik analizy.
    
    Poniżej znajduje się przykładowa funkcja (placeholder):
    """
    # Przykładowy kod – zastąp to własną integracją:
    model_api_url = "https://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/analiza"
    payload = {
        "prompt": f"Przeanalizuj poniższy kod z pliku {file_path} i podaj wnioski dotyczące jego struktury, potencjalnych problemów oraz możliwych usprawnień w kontekście funkcjonalności całego narzedzia, które jest menadżerem życia z uwzględnieniem zaburzeń psychicznych - mocnym ADHD użytkownika - Rafała Bartosika.:\n\n{code}",
        "model": "o3-mini-high",
        "options": {"reasoning": "deep"}
    }
    # Wyślij zapytanie POST do API modelu
    response = requests.post(model_api_url, json=payload)
    response.raise_for_status()
    result = response.json()
    return result.get("analysis", "Brak analizy")

if __name__ == "__main__":
    traverse_repo()

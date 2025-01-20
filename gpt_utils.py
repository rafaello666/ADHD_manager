import os
from openai import OpenAI
from tasks import get_all_tasks

def suggest_order_with_gpt():
   
    # Inicjalizujemy klienta OpenAI
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    # Pobieramy zadania
    tasks_list = get_all_tasks()

    # Konstruujemy tekst z listą zadań (np. w formie bullet list)
    tasks_str 
    for t in tasks_list:
        status = "ukończone" if t.get('completed') else "nieukończone"
        tasks_str += f"- {t['id']}: {t['title']} (status: {status})\n"

    # messages – styl chatowy
    # "developer" rola to Twój custom – w API OpenAI często używa się: system/assistant/user
    # Tutaj stosujemy się do Twojego wzoru "role": "developer".
    messages = [
        {
            "role": "developer",
            "content": "You are a helpful assistant. Provide an optimal order for the tasks, with explanation."
        },
        {
            "role": "user",
            "content": (
                f"I have these tasks:\n{tasks_str}\n"
                "Please provide an optimal order and explain why."
            )
        }
    ]

    # Wywołanie chat.completions.create z modelem 'gpt-4o'
    

    # Zwracamy treść wiadomości z pierwszego wyboru
    return completion.choices[0].message["content"]

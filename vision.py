from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "http://127.0.0.1:5000/static/layout.jpg"
                    },
                },
            ],
        }
    ],
    max_tokens=400,
)

print(response.choices[0])
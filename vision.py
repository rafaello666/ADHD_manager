from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
messages=[
        {
            "role": "user",
            "content": [
                {
                "type": "text", 
                "text": (
                    "Describe as many as you can see on this image."          
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://szczepanek-modelki.com/srronka.jpg"
                    }
                }
            ]
        }
            ],
        
    
    max_tokens=5900,
    temperature=0.05
)

print(response.choices[0])
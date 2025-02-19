from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
messages=[
        {
            "role": "user",
            "content": [
                {
                "type": "text", "text": "Describe everything visible on this website screenshot. You are a Vision model that sees the image content. Please provide the most thorough and detailed description possible,  including layout, colors, text, structure, and any noticeable design elements. Focus on describing any text in Polish as accurately as possible,   and note key visual details.  Break down your description into clear sections."
                },
                {
                    "type": "image_url",
                    "image_url": 
                        "url": "https://szczepanek-modelki.com/kolaz.jpg"
                    }
            ]
        }
    ],
    max_tokens=3500,
    temperature=0.05
)
print(response.choices[0])
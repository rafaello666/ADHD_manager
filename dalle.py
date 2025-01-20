from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="""generate a UI color palette for a bold, edgy task manager""",





    size="1024x1024",
    quality="hd",
    n=1,
)

print(response.data[0].url)
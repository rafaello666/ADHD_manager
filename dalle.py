from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="""A modern, minimalist logo for an application called 'ADHD_Manager', symbolizing focus, productivity, and well-being. Use bright, uplifting colors (like teal, yellow, or vibrant purple), simple geometric shapes, and a clean tech-inspired aesthetic. The design should incorporate a subtle hint of a brain outline or a heartbeat/HRV line, reflecting mental health and personal monitoring. Aim for a balanced composition that works well as an app icon, with a slightly playful yet professional vibe. Incorporate subtle circuit patterns. No text.""",





    size="1024x1024",
    quality="hd",
    n=1,
)

print(response.data[0].url)
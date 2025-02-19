from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="""Design a modern and minimalistic icon for a PDF file. The icon should feature:

A red document outline with folded top-right corner, symbolizing a file.
A large, bold text 'PDF' in white letters centered on the document.
A simple, clean style with flat design principles.
Background: transparent or white, suitable for use on both light and dark themes.
Dimensions: square aspect ratio (512x512 or larger) for scalability.""",





    size="1024x1024",
    quality="hd",
    n=1,
)

print(response.data[0].url)
from PIL import Image, ImageDraw, ImageFont
import random

# Otwieramy istniejący obraz:
image = Image.open("monix.jpeg")

draw = ImageDraw.Draw(image)

# Większy rozmiar czcionki
font_size = 100
font = ImageFont.truetype("arial.ttf", font_size)

text = "DOBRANOC MONIA"

# Ustalamy błękitny kolor tekstu (np. #9ADCFF)
text_color = (154, 220, 255)

# Obliczamy wymiary tekstu za pomocą getbbox
bbox = font.getbbox(text)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x_pos = (image.width - text_width) // 2
y_pos = 50

# Rysujemy niebieski napis
draw.text((x_pos, y_pos), text, font=font, fill=text_color)

# Dodajemy losowe "brokatowe" kropki w obrębie tekstu (prosty efekt)
for _ in range(200):
    sparkle_x = random.randint(x_pos, x_pos + text_width)
    sparkle_y = random.randint(y_pos, y_pos + text_height)
    # Jasny kolor iskier
    sparkle_color = (255, 255, 200)
    draw.point((sparkle_x, sparkle_y), fill=sparkle_color)

# Zapisujemy nowy obraz
image.save("image_with_text.jpeg")

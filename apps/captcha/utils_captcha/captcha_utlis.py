from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import io
import base64

def generate_captcha_text(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha_image(text): 
    width, height = 200, 80
    background_color = (255, 255, 255)
    font_color = (60, 80, 200)
    font_size = 48
    font_path = r"C:\Users\marin\Downloads\dejavu-fonts-ttf-2.37\dejavu-fonts-ttf-2.37\ttf\DejaVuSansMono-Bold.ttf"

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Criar imagem do texto separado para rotacionar
    text_img = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((0, 0), text, font=font, fill=font_color)

    # Rotação leve e aleatória entre -15 e 15 graus
    angle = random.uniform(-15, 15)
    rotated_text = text_img.rotate(angle, resample=Image.BICUBIC, expand=1)

    # Colar texto rotacionado na imagem principal centralizado
    rx, ry = rotated_text.size
    image.paste(rotated_text, ((width - rx) // 2, (height - ry) // 2), rotated_text)

    # Pontos coloridos aleatórios para confundir
    for _ in range(300):  # Aumentei de 200 para 300
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    # Linhas com mais variação e mais linhas
    for _ in range(5):  # De 3 para 5 linhas
        points = []
        x = random.randint(0, width)
        y = random.randint(0, height)
        for _ in range(6):  # De 5 para 6 pontos por linha
            x += random.randint(-25, 25)
            y += random.randint(-25, 25)
            points.append((x, y))
        draw.line(points, fill=font_color, width=2)

    # Distorção mais agressiva
    

    image = image.filter(ImageFilter.GaussianBlur(1.2))  # Blur um pouco mais forte

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str



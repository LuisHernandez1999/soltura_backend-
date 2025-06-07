import random
import string
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import hashlib

def gerar_texto_captcha(tamanho=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def gerar_imagem_captcha(texto):
    largura, altura = 150, 50
    imagem = Image.new('RGB', (largura, altura), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.load_default()

    draw.text((10, 10), texto, font=fonte, fill=(0, 0, 0))

    
    for _ in range(5):
        draw.line([
            (random.randint(0, largura), random.randint(0, altura)),
            (random.randint(0, largura), random.randint(0, altura))
        ], fill=(0, 0, 0), width=1)

    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode()
    return imagem_base64

def hash_captcha(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

import random, string, hashlib
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha_image(text):
    img = Image.new('RGB', (150, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))
##
    for _ in range(8):
        draw.line([
            random.randint(0, 150), random.randint(0, 50),
            random.randint(0, 150), random.randint(0, 50)
        ], fill=(0, 0, 0), width=1)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def hash_captcha(text):
    return hashlib.sha256(text.encode()).hexdigest()

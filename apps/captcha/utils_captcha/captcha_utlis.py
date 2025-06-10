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
    spacing = -6  

    font = ImageFont.truetype(font_path, font_size)

    letters = []
    total_width = 0
    for char in text:
        bbox = font.getbbox(char)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]

        char_img = Image.new('RGBA', (char_width + 20, char_height + 20), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((10, 10), char, font=font, fill=font_color)
        scale_x = random.uniform(0.6, 0.85)
        scale_y = random.uniform(0.8, 1.0)
        scaled = char_img.resize((int(char_img.width * scale_x), int(char_img.height * scale_y)), resample=Image.BICUBIC)

        angle = random.uniform(-25, 25)
        rotated = scaled.rotate(angle, resample=Image.BICUBIC, expand=1)

        letters.append(rotated)
        total_width += rotated.size[0] + spacing

    total_width -= spacing

    image = Image.new('RGB', (max(width, total_width + 20), height), background_color)
    draw = ImageDraw.Draw(image)

    current_x = (image.width - total_width) // 2
    for letter in letters:
        y_offset = random.randint(-5, 5)
        image.paste(letter, (current_x, (height - letter.size[1]) // 2 + y_offset), letter)
        current_x += letter.size[0] + spacing

    for _ in range(300):
        x = random.randint(0, image.width - 1)
        y = random.randint(0, image.height - 1)
        draw.point((x, y), fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    for _ in range(5):
        points = []
        x = random.randint(0, image.width)
        y = random.randint(0, image.height)
        for _ in range(6):
            x += random.randint(-25, 25)
            y += random.randint(-25, 25)
            points.append((x, y))
        draw.line(points, fill=font_color, width=2)

    image = image.filter(ImageFilter.GaussianBlur(1.2))

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str
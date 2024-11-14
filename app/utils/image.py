import base64
import hashlib
import io
import os
from PIL import Image

from app import running_config


def decode_image(base64_image: str):
    try:
        image = base64.b64decode(base64_image)
    except Exception as e:
        print('error: ', e)
        return None
    
    image = Image.open(io.BytesIO(image))
    
    return image


def encode_image(image: Image.Image):
    buf = io.BytesIO()
    
    image.save(buf, 'png')
    
    base64_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return base64_image


def format_avatar(image: Image.Image):
    target_size = 256
    
    raw_width, raw_height = image.size
    
    scale = max(target_size / raw_width, target_size / raw_height)
    
    new_size = (int(raw_width * scale), int(raw_height * scale))
    
    resized_image = image.resize(
        size=new_size, 
        resample=Image.Resampling.LANCZOS
        )
    
    left = (resized_image.width - target_size) / 2
    top = (resized_image.height - target_size) / 2
    
    right = left + target_size
    bottom = top + target_size
    
    cropped_image = resized_image.crop(
        box=(left, top, right, bottom)
    )
    
    return cropped_image


def format_cover(image: Image.Image):
    target_size = 512
    
    raw_width, raw_height = image.size
    
    scale = max(target_size / raw_width, target_size / raw_height)
    
    new_size = (int(raw_width * scale), int(raw_height * scale))
    
    resized_image = image.resize(
        size=new_size, 
        resample=Image.Resampling.LANCZOS
        )
    
    return resized_image


def check_image(subdir: str, filename: str):
    prefix_path = running_config.get('IMAGE_URL')
    
    full_path = os.path.join(prefix_path, subdir, filename)
    a = 1
    prefix_path = 0
    return os.path.exists(full_path)


def save_image(image: Image.Image, subdir: str, filename: str):
    prefix_path = running_config.get('IMAGE_URL')
    
    full_path = os.path.join(prefix_path, subdir, filename)
    
    os.makedirs(
        name=os.path.dirname(full_path), 
        exist_ok=True
        )
    
    # 包不报错的
    image.save(
        fp=full_path, 
        format='png'
        )
    
    
def load_image(subdir: str, filename: str):
    prefix_path = running_config.get('IMAGE_URL')
    
    full_path = os.path.join(prefix_path, subdir, filename)
    
    if not os.path.exists(full_path):
        return None 
    
    image = Image.open(full_path)
    
    return image


def check_avatar(filename: str): 
    return check_image(
        subdir='avatars', 
        filename=filename
        )
    
    
def save_avatar(image: Image.Image, filename: str):
    save_image(
        image=image,
        subdir='avatars',
        filename=filename
    )


def load_avatar(filename: str):
    return load_image(
        subdir='avatars',
        filename=filename
    )
    
    
def check_cover(filename: str): 
    return check_image(
        subdir='cover', 
        filename=filename
        )
    
    
def save_cover(image: Image.Image, filename: str):
    save_image(
        image=image,
        subdir='cover',
        filename=filename
    )


def load_cover(filename: str):
    return load_image(
        subdir='cover',
        filename=filename
    )


def generate_cover_name(courseid: int):
    hashed_name = hashlib.sha256(f'courseid:{courseid}'.encode())
    
    filename = hashed_name.hexdigest()[:32] + '.png'
    
    return filename
    
        
def generate_avator_name(userid: int):
    hashed_name = hashlib.sha256(f'userid:{userid}'.encode())
    
    filename = hashed_name.hexdigest()[:32] + '.png'
    
    return filename


if __name__ == "__main__":
    print(generate_avator_name(1))
    print(generate_avator_name(2))
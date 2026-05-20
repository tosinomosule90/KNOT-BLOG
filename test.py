import os
from flask import current_app
import secrets

def save_picture(form_picture, old_picture=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize image before saving (Optional but recommended)
    # from PIL import Image
    # i = Image.open(form_picture)
    # i.thumbnail((250, 250))
    # i.save(picture_path)
    
    form_picture.save(picture_path)

    # Delete the old picture if it exists and isn't the default
    if old_picture and old_picture != 'default.jpg':
        old_path = os.path.join(current_app.root_path, 'static/profile_pics', old_picture)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except OSError:
                # Handle cases where the file might be in use or already gone
                pass

    return picture_fn

def save_media(form_file, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(current_app.root_path, 'static', folder, filename)
    form_file.save(filepath)
    return filename
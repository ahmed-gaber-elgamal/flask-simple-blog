import os
from PIL import Image
from flask import url_for, current_app


def add_post_pic(pic_uplaod, title):
    filename = pic_uplaod.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(title)+'.'+ext_type
    file_path = os.path.join(current_app.root_path, 'static/post_pics', storage_filename)
    output_size = (200, 200)
    pic = Image.open(pic_uplaod)
    pic.thumbnail(output_size)
    pic.save(file_path)
    return storage_filename

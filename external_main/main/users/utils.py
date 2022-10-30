import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from main import mail


def save_picture(form_pic, img_path='profile_pics'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/{img_path}',
                                picture_fn)
    img = Image.open(form_pic)
    if img_path == 'profile_pics':
        output_size = (125, 125)
        img.thumbnail(output_size)

    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
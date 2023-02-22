from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired(),
                                    Length(min=10, max=100)])
    content = TextAreaField("Content", validators=[DataRequired()])
    picture = FileField("Profile Image",
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Post")

class PostComment(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Comment")
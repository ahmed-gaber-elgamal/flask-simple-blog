from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, RadioField, SelectField, TextField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed


class BlogPostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text = TextAreaField('text', validators=[DataRequired()])
    picture = FileField('Upload Post picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Bookmarks

class BookmarkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    tags = StringField('Tag(s)', validators=[DataRequired()])
    submit = SubmitField('Save')
    
    def validate_title(self, title):
        t = Bookmarks.query.filter_by(title=title.data).first()
        if t is not None:
            raise ValidationError("You already have this")

    def validate_link(self, link):
        l = Bookmarks.query.filter_by(link=link.data).first()
        if l is not None:
            raise ValidationError("You already have this")

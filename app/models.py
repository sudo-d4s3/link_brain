from app import db

tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
        db.Column('boodmark_id', db.Integer, db.ForeignKey('bookmarks.id'), primary_key=True)
)

class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), index=True, unique=True)
    link = db.Column(db.String, index=True, unique=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
            backref=db.backref('bookmark', lazy=True))

    def __repr__(self):
        return '<Bookmarks {}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

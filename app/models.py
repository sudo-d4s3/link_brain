from app import db

class Bookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), index=True, unique=True)
    link = db.Column(db.String, index=True, unique=True)
    tags = db.Column(db.String, index=True)

    def __repr__(self):
        return '<Bookmarks {}>'.format(self.title)

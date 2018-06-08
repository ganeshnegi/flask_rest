from project import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.id

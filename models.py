from flask_sqlalchemy import SQLAlchemy
import hashlib, string, random

db = SQLAlchemy()

class Link(db.Model):
    id = db.Column(db.String(7), primary_key=True)

    full_link = db.Column(db.String(2048))

    def __init__(self, full_link):
        self.full_link = full_link

        self.id = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=7))

if __name__ == "__main__":
    db.create_all()

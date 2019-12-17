# services/pokemon/project/api/models.py

from sqlalchemy.dialects.postgresql import ARRAY

from project import db


class Pokemon(db.Model):
    __tablename__ = "pokemon"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    abilities = db.Column(ARRAY(db.String))
    thumbnail_alt_text = db.Column(db.String)
    weakness = db.Column(ARRAY(db.String))
    number = db.Column(db.String)
    height = db.Column(db.Integer)
    collectibles_slug = db.Column(db.String)
    featured = db.Column(db.String)
    thumbnail_image = db.Column(db.String)
    type = db.Column(ARRAY(db.String))
    slug = db.Column(db.String)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight': self.weight,
            'abilities': self.abilities,
            'thumbnail_alt_text': self.thumbnail_alt_text,
            'weakness': self.weakness,
            'number': self.number,
            'height': self.height,
            'collectibles_slug': self.collectibles_slug,
            'featured': self.featured,
            'thumbnail_image': self.thumbnail_image,
            'type': self.type,
            'slug': self.slug
        }

    def __init__(self, name, weight, abilities, thumbnail_alt_text, weakness, number, height, collectibles_slug, featured, thumbnail_image, type, slug):
        self.name = name
        self.weight = weight
        self.abilities = abilities
        self.thumbnail_alt_text = thumbnail_alt_text
        self.weakness = weakness
        self.number = number
        self.height = height
        self.collectibles_slug = collectibles_slug
        self.featured = featured
        self.thumbnail_image = thumbnail_image
        self.type = type
        self.slug = slug
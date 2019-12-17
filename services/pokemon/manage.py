# services/pokemon/manage.py

import json
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Pokemon

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def seed_db():
    """Seed pokemon database"""
    with open('./data.json') as f:
        datas = json.load(f)
        for data in datas:
            print(data)
            db.session.add(
                Pokemon(
                    name=data["name"],
                    weight=data["weight"],
                    abilities=data["abilities"],
                    thumbnail_alt_text=data["ThumbnailAltText"],
                    weakness=data["weakness"],
                    number=data["number"],
                    height=data["height"],
                    collectibles_slug=data["collectibles_slug"],
                    featured=data["featured"],
                    thumbnail_image=data["ThumbnailImage"],
                    type=data["type"],
                    slug=data["slug"]
                )
            )
        db.session.commit()

if __name__ == '__main__':
    # start the flask application
    cli()
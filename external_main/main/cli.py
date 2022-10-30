import click
from flask import Blueprint
from main.models import User, Post
from main import db


bp = Blueprint('commands', __name__)

@bp.cli.command("say_my_name")
@click.option('-name', default="Noname")
def say_my_name(name):
    print("say_my_name %s " % name)

@bp.cli.command("create_db")
@click.option('-name', default="Noname")
def create_db(name):
    print("creating db %s " % name)
    db.drop_all()
    db.create_all()
    db.session.commit()

import pyodbc
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = pyodbc.connect('DRIVER={SQL Server};SERVER=QUANTO-12;DATABASE=SysetiQuanto;Trusted_Connection=Yes;')
        g.c = g.db.cursor()
    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
        print(i)

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
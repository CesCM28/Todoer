#from functools import _Descriptor
from logging import error
from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id,t.description,u.username,t.completed,t.created_at from todo t JOIN users u on t.created_by = u.id WHERE created_by = ? order by t.created_by desc', (g.user[0])
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Descripción es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'INSERT INTO dbo.todo (created_by, created_at, description, completed) VALUES( ?, GETDATE(), ?, ?)', (g.user[0], description, False)
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


def get_todo(id):
    db, c = get_db()
    c.execute(
        'SELECT t.id,t.description,t.completed,t.created_by,u.username FROM dbo.todo t INNER JOIN dbo.users u ON t.created_by = u.id WHERE t.id = ?', (id)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "El todo de id {0} no existe.".format(id))

    return todo


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = 'La descripcíon es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'UPDATE dbo.todo SET description = ?, completed = ? WHERE id = ? AND created_by = ', (description, completed, id, g.user[0])
            )
            db.commit()
            print('estamos funcionando')
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    print(id)
    db, c = get_db()
    c.execute(
        'DELETE FROM dbo.todo WHERE id = ? AND created_by = ?', (id, g.user[0])
    )
    db.commit()
    return redirect(url_for('todo.index'))
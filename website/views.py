from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# home function runs, whenever we go to '/' directory


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(title=title, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updateNote(id):
    if request.method == 'POST':
        title = request.form['title']
        data = request.form['note']
        note = Note.query.filter_by(id=id).first()
        note.title = title
        note.data = data
        db.session.add(note)
        db.session.commit()
        return render_template("home.html", user=current_user)

    note_update = Note.query.filter_by(id=id).first()
    return render_template("update.html", nu=note_update, user=current_user)

from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user, logout_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

# Define the "home" function, which runs whenever we go to the "/" directory.


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # If a POST request is received, retrieve the note's title and content from the submitted form.
    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        # create a new Note object with the current user's ID, add it to the database, and flash a success message.
        else:
            new_note = Note(title=title, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    # Render the "home.html" template with the current user's information.
    return render_template("home.html", user=current_user)

# Define the "delete_note" function, which deletes a note with the given ID.


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Parse the request's JSON data to retrieve the note's ID.
    note = json.loads(request.data)
    noteId = note['noteId']
    # Retrieve the corresponding Note object from the database.
    note = Note.query.get(noteId)
    # If the Note object exists and belongs to the current user, delete it from the database and commit the changes.
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # Return an empty JSON response.
    return jsonify({})
# Define the "updateNote" function, which updates a note with the given ID.


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updateNote(id):
    # If a POST request is received, retrieve the updated note's title and content from the submitted form,
    # update the corresponding Note object's title and content, add it to the database, and commit the changes.
    # Then, render the "home.html" template with the current user's information.
    if request.method == 'POST':
        title = request.form['title']
        data = request.form['note']
        note = Note.query.filter_by(id=id).first()
        note.title = title
        note.data = data
        db.session.add(note)
        db.session.commit()
        return render_template("home.html", user=current_user)
    # If a GET request is received, retrieve the corresponding Note object from the database and render the
    # "update.html" template with the Note object and the current user's information.
    note_update = Note.query.filter_by(id=id).first()
    return render_template("update.html", nu=note_update, user=current_user)


@views.route("/deleteAcc/<int:id>", methods=['GET', 'POST'])
@login_required
def deleteACC(id):
    user = User.query.filter_by(id=id).first()
    if user:
        if len(user.notes) > 0:
            notes = Note.query.filter_by(user_id=user.id).all()
            for note in notes:
                db.session.delete(note)
                db.session.commit()
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Account is successfully deleted", category="success")
    return render_template("login.html", user=current_user)

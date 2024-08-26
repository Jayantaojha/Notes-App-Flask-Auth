from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            note = data.get('note')
        elif request.content_type == 'text/plain':
            note = request.data.decode('utf-8')
        else:
            note = request.form.get('note-input')

        if not note or len(note) < 1:
            return jsonify({"success": False, "message": "Note is too short!"}), 400

        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()

        return jsonify({"success": True, "message": "Note added successfully!"}), 200

    # Fetch notes ordered by date in descending order
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()
    return render_template('home.html', user=current_user, notes=notes)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            noteId = data.get('noteid')
        
            note = Note.query.get(noteId)

            if note:
                if note.user_id == current_user.id:
                    db.session.delete(note)
                    db.session.commit()
            
            return jsonify({
                "success" : True,
                "message" : "Note deleted successfully!" 
            }), 200
            


@views.route('/update-note', methods=['POST'])
def update_note():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            noteId = data.get('noteid')
        
            note = Note.query.get(noteId)

            if note:
                if note.user_id == current_user.id:
                    db.session.delete(note)
                    db.session.commit()
            
            return jsonify({
                "success" : True,
                "message" : "Note deleted successfully!" 
            }), 200
            
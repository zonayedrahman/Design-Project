from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Interest
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return render_template("home.html", user=current_user)
    return render_template("home.html", user=current_user)


@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        return render_template("settings.html", user=current_user)
    return render_template("settings.html", user=current_user)


@views.route('/interests', methods=['GET', 'POST'])
@login_required
def interests():
    if request.method == 'POST':
        interest = request.form.get('interest_menu')  # Gets the new interest from the HTML

        new_interest = Interest(name=interest, user_id=current_user.id)  # providing the schema for the note
        db.session.add(new_interest)  # adding the note to the database
        db.session.commit()
        flash('Interest added!', category='success')

    f = open(r'C:\Users\Zonayed\Documents\GitHub\Design-Project\app\static\hobbies.txt')

    try:
        # do stuff with f
        dic = f.readlines()
    finally:
        f.close()
    return render_template("interests.html", user=current_user, hobbies=dic)


@views.route('/delete-interest', methods=['POST'])
def delete_interest():
    interest = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    interestId = interest['interestId']
    note = Interest.query.get(interestId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

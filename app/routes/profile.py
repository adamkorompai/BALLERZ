from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def view_profile():
    return render_template('profile/view.html', user=current_user)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Check if username or email is already taken
        if username != current_user.username and User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('profile.edit_profile'))
            
        if email != current_user.email and User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('profile.edit_profile'))
            
        try:
            current_user.username = username
            current_user.email = email
            db.session.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('profile.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.')
            return redirect(url_for('profile.edit_profile'))
            
    return render_template('profile/edit.html', user=current_user)

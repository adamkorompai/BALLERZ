from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        try:
            # Create new user with initial password
            new_user = User(username=username, password='')
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Add debug print
            db.session.rollback()
            flash('An error occurred. Please try again.')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.welcome'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.welcome'))
        flash('Invalid username or password')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.cli.command('create-test-user')
def create_test_user():
    """Create a test user."""
    try:
        user = User(username='test')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()
        print("Test user created successfully!")
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.session.rollback() 
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.event import Event
from models.registration import Registration
import mysql.connector
from functools import wraps
from database.db import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        print(admin)
        cursor.close()
        conn.close()
        
        if admin:
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid credentials')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    events = Event.get_all()
    return render_template('admin/dashboard.html', events=events)

@admin_bp.route('/events/add', methods=['GET', 'POST'])
@admin_required
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        venue = request.form['venue']
        date = request.form['date']
        time = request.form['time']
        max_participants = request.form['max_participants']
        
        Event.create(name, description, category_id, venue, date, time, max_participants)
        return redirect(url_for('admin.dashboard'))
    
    categories = Event.get_categories()
    return render_template('admin/event_form.html', categories=categories, event=None)

@admin_bp.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    event = Event.get_by_id(event_id)
    
    if not event:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']
        venue = request.form['venue']
        date = request.form['date']
        time = request.form['time']
        max_participants = request.form['max_participants']
        
        Event.update(event_id, name, description, category_id, venue, date, time, max_participants)
        return redirect(url_for('admin.dashboard'))
    
    categories = Event.get_categories()
    return render_template('admin/event_form.html', categories=categories, event=event)

@admin_bp.route('/events/delete/<int:event_id>')
@admin_required
def delete_event(event_id):
    Event.delete(event_id)
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/events/participants/<int:event_id>')
@admin_required
def view_participants(event_id):
    event = Event.get_by_id(event_id)
    participants = Registration.get_participants_by_event(event_id)
    return render_template('admin/participants_list.html', event=event, participants=participants)
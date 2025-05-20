from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.event import Event
from models.student import Student
from models.registration import Registration
import mysql.connector

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/events')
def events_list():
    events = Event.get_all()
    print(events)
    return render_template('student/events_list.html', events=events)

@student_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        email = request.form['email']
        phone = request.form['phone']

         # Validate phone number length
        if len(phone) != 10 or not phone.isdigit():
            events = Event.get_all()
            return render_template('student/registration_form.html', 
                                   events=events, 
                                   error="Phone number must be exactly 10 digits.")
        
        event_ids = request.form.getlist('events')
        
        if not event_ids:
            events = Event.get_all()
            return render_template('student/registration_form.html', 
                                 events=events, 
                                 error="Please select at least one event.")
        
        try:
            student_id = Student.create(name, usn, email, phone)
            
            Registration.register_student_for_events(student_id, event_ids)
            
            return redirect(url_for('student.registration_success', usn=usn))
        
        except mysql.connector.Error as e:
            events = Event.get_all()
            return render_template('student/registration_form.html', 
                                 events=events, 
                                 error=f"Database error: {str(e)}")
    
    events = Event.get_all()
    return render_template('student/registration_form.html', events=events)

@student_bp.route('/register/success')
def registration_success():
    usn = request.args.get('usn', '')
    if usn:
        student = Student.get_by_usn(usn)
        if student:
            registered_events = Registration.get_events_by_student(student['id'])
            return render_template('student/registration_success.html', 
                                 student=student, 
                                 events=registered_events)
    
    return redirect(url_for('student.events_list'))
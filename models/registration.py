from database.db import get_db_connection
import mysql.connector

class Registration:
    @staticmethod
    def register_student_for_events(student_id, event_ids):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for event_id in event_ids:
            try:
                cursor.execute('''
                    INSERT INTO registration (student_id, event_id)
                    VALUES (%s, %s)
                ''', (student_id, event_id))
            except mysql.connector.IntegrityError:
                pass
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def get_participants_by_event(event_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT s.*, r.registration_date
            FROM registration r
            JOIN student s ON r.student_id = s.id
            WHERE r.event_id = %s
            ORDER BY r.registration_date
        ''', (event_id,))
        participants = cursor.fetchall()
        cursor.close()
        conn.close()
        return participants
    
    @staticmethod
    def get_events_by_student(student_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT e.*, c.name AS category_name, r.registration_date
            FROM registration r
            JOIN event e ON r.event_id = e.id
            LEFT JOIN event_category c ON e.category_id = c.id
            WHERE r.student_id = %s
        ''', (student_id,))
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        return events
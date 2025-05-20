from database.db import get_db_connection

class Student:
    @staticmethod
    def create(name, usn, email, phone):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM student WHERE usn = %s', (usn,))
        existing_student = cursor.fetchone()
        
        if existing_student:
            student_id = existing_student[0]
        else:
            cursor.execute('''
                INSERT INTO student (name, usn, email, phone)
                VALUES (%s, %s, %s, %s)
            ''', (name, usn, email, phone))
            student_id = cursor.lastrowid
            conn.commit()
        
        cursor.close()
        conn.close()
        return student_id
    
    @staticmethod
    def get_by_usn(usn):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student WHERE usn = %s', (usn,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        return student
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students
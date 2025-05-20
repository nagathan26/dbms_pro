from database.db import get_db_connection

class Event:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT e.*, c.name AS category_name 
            FROM event e 
            LEFT JOIN event_category c ON e.category_id = c.id
        ''')
        events = cursor.fetchall()
       
        cursor.close()
        conn.close()
        return events
    
    @staticmethod
    def get_by_id(event_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT e.*, c.name AS category_name 
            FROM event e 
            LEFT JOIN event_category c ON e.category_id = c.id
            WHERE e.id = %s
        ''', (event_id,))
        event = cursor.fetchone()
        cursor.close()
        conn.close()
        return event
    
    @staticmethod
    def create(name, description, category_id, venue, date, time, max_participants):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO event (name, description, category_id, venue, date, time, max_participants)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, description, category_id, venue, date, time, max_participants))
        event_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return event_id
    
    @staticmethod
    def update(event_id, name, description, category_id, venue, date, time, max_participants):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE event 
            SET name = %s, description = %s, category_id = %s, venue = %s, date = %s, time = %s, max_participants = %s
            WHERE id = %s
        ''', (name, description, category_id, venue, date, time, max_participants, event_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def delete(event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM event WHERE id = %s', (event_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @staticmethod
    def get_categories():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM event_category')
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories
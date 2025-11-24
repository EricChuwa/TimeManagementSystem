import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnector:
    def __init__(self):
        self.config = {
            'host': 'apex-2025-ekco-2048.e.aivencloud.com',
            'user': 'avnadmin',
            'password': os.getenv('DB_PASS'),
            'port': 21911,
            'database': 'KRONOS',
            'ssl_disabled' : True
        }
        self.connection = None
        self.cursor = None

        
        

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return self.connection

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    # Task methods
    def add_task(self, title, deadline, estimated_hours, status='Pending'):
        
        sql = """
                INSERT INTO tasks (title, deadline, estimated_hours, status) VALUES (%s, %s, %s, %s)
                """
        self.cursor.execute(sql, (title, deadline, estimated_hours, status))
        self.connection.commit()
        

    def edit_task(self, task_id, **kwargs):
        
        
        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(f"{key}=%s")
            values.append(value)

        values.append(task_id)

        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id=%s"

        self.cursor.execute(sql, tuple(values))
        self.connection.commit()
        

    def remove_task(self, task_id): 
        
        sql = "DELETE FROM tasks WHERE id=%s"
        self.cursor.execute(sql, (task_id,))
        self.connection.commit()
        

    def fetch_tasks(self): 
        
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        

        return tasks

    def fetch_task_by_id(self, task_id):
        
        self.cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        task = self.cursor.fetchone()
        

        return task

    def fetch_tasks_by_status(self, status): 
        
        self.cursor.execute("SELECT * FROM tasks WHERE status=%s", (status,))
        tasks = self.cursor.fetchall()
        

        return tasks

    def fetch_tasks_due_soon(self, days=3):
        
        sql = """
            SELECT * FROM tasks
            WHERE deadline <= CURDATE() + INTERVAL %s DAY AND status!='Completed'
            ORDER BY deadline ASC
        """
        self.cursor.execute(sql, (days,))
        tasks = self.cursor.fetchall()
        

        return tasks

    def fetch_tasks_by_module(self, module_name):
        
        self.cursor.execute("SELECT * FROM tasks WHERE module=%s", (module_name,))
        tasks = self.cursor.fetchall()
        

        return tasks
    
    def fetch_overdue_tasks(self):
        
        sql = "SELECT * FROM tasks WHERE deadline < CURDATE() AND status!='Completed'"
        self.cursor.execute(sql)
        tasks = self.cursor.fetchall()
        

        return tasks

    # Add Study Session
    def add_session(self, task_id, start_time, end_time, duration_minutes, session_type='work'):
        self.connect()
        
        try:
            
            sql = """
                INSERT INTO sessions (task_id, start_time, end_time, duration_minutes, session_type) VALUES (%s, %s, %s, %s, %s)
                """
            self.cursor.execute(sql, (task_id, start_time, end_time, duration_minutes, session_type))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding session: {e}")
            return False  # failure
        finally:
            print("")
             

    def edit_session(self, session_id, **kwargs): 
        self.connect()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key}=%s")
            values.append(value)
        values.append(session_id)
        sql = f"UPDATE sessions SET {', '.join(fields)} WHERE id=%s"
        self.cursor.execute(sql, tuple(values))
        self.connection.commit()
        
        
    def remove_session(self, session_id):
        self.connect()
        
        sql = "DELETE FROM sessions WHERE id=%s"
        self.cursor.execute(sql, (session_id,))
        self.connection.commit()
         

    def fetch_sessions_by_task(self, task_id): 
        self.connect()
        
        self.cursor.execute("SELECT * FROM sessions WHERE task_id=%s", (task_id,))
        sessions = self.cursor.fetchall()
        
        return sessions

    def fetch_sessions(self): 
        self.connect()
        
        self.cursor.execute("SELECT * FROM sessions")
        sessions = self.cursor.fetchall()
        
        return sessions

    def fetch_sessions_by_date_range(self, start_date, end_date):
        self.connect()
        
        sql = """
            SELECT * FROM sessions
            WHERE start_time >= %s AND end_time <= %s
        """
        self.cursor.execute(sql, (start_date, end_date))
        sessions = self.cursor.fetchall()
        

        return sessions
    
    def fetch_session_by_id(self, session_id):
        self.connect()
        self.cursor.execute("SELECT * FROM sessions WHERE id=%s", (session_id,))
        session = self.cursor.fetchone()
        
        return session

    # Analytics
    def total_study_hours(self):
        self.connect()
        sql = "SELECT SUM(duration_minutes) AS total_minutes FROM sessions WHERE session_type='work'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result and result['total_minutes']:
            return round(result['total_minutes'] / 60, 2)  # hours as float
        else:
            return 0

    def completion_rate(self):
        self.connect()
        sql_total = "SELECT COUNT(*) AS total FROM tasks"
        sql_completed = "SELECT COUNT(*) AS completed FROM tasks WHERE status='Completed'"
        self.cursor.execute(sql_total)
        total = self.cursor.fetchone()['total']
        self.cursor.execute(sql_completed)
        completed = self.cursor.fetchone()['completed']
        
        if total == 0:
            return 0
        
        return round((completed / total) * 100, 2)  # percent

    def average_session_length(self):
        self.connect()
        sql = "SELECT AVG(duration_minutes) AS avg_minutes FROM sessions WHERE session_type='work'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result and result['avg_minutes']:
            return round(result['avg_minutes'], 2)
        else:
            return 0

    def most_productive_day(self):
        self.connect()
        sql = """
            SELECT DATE(start_time) AS study_day, SUM(duration_minutes) AS minutes
            FROM sessions
            WHERE session_type='work'
            GROUP BY study_day
            ORDER BY minutes DESC
            LIMIT 1
        """
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        if result:
            return result['study_day'], result['minutes']
        else:
            return None, 0

    def tasks_completed_on_time(self):
        self.connect()
        sql = """
            SELECT COUNT(*) AS on_time
            FROM tasks
            WHERE status='Completed' AND updated_at <= deadline
        """
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        
        return result['on_time'] if result else 0

    # Reflection Access
    def add_reflection(self, week_start, week_end, reflection_text): 
        self.connect()
        sql = """
            INSERT INTO reflections (week_start, week_end, reflection_text)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (week_start, week_end, reflection_text))
        self.connection.commit()
        

    def fetch_reflections(self): 
        self.connect()
        self.cursor.execute("SELECT * FROM reflections ORDER BY week_start DESC")
        reflections = self.cursor.fetchall()
        
        return reflections
        
    def edit_reflection(self, reflection_id, reflection_text): 
        self.connect()
        sql = "UPDATE reflections SET reflection_text=%s WHERE id=%s"
        try:
            self.cursor.execute(sql, (reflection_text, reflection_id))
            self.connection.commit()
            
            return True
        except Exception as e:
            print("Error updating",e)
            return False

    def remove_reflection(self, reflection_id):
        self.connect()
        sql = "DELETE FROM reflections WHERE id=%s"
        self.cursor.execute(sql, (reflection_id,))
        self.connection.commit()
        

con = DatabaseConnector()
con.connect()
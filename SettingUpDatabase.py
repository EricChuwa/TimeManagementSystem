import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() # Loads the env fil



class DatabaseBuilder:
    def __init__(self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASS = os.getenv('DB_PASS')
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_PORT = int(os.getenv("DB_PORT"))

        self.config = {
            'host' : self.DB_HOST,
            'user' : self.DB_USER,
            'password' : self.DB_PASS,
            'port': self.DB_PORT,
            'ssl_disabled': True
        }

        self.con = None
        self.cursor = None
    
    def connect(self):
        try:
            self.con = mysql.connector.connect(**self.config)
            if self.con.is_connected():
                print("Connection Status: Succesful")
                self.cursor = self.con.cursor(dictionary=True)
        except Exception as e:
            print(f"Error: {e}")
        return self.con
    
    def create_db(self):
        # Create the Kronos Database if it doesn't exist
        try:
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}"
            )
            print(f"Database '{self.DB_NAME}' has been created!")

            # Selecting Database
            self.cursor.execute(
                f"USE {self.DB_NAME};"
            )
        except Exception as e:
            print(f"Failed creating Database: {e}")
            raise

    def create_tables(self):
        # Creating the tasks, sessions, and reflections table.
        TABLES = {}

        # tasks
        TABLES["tasks"] = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                deadline DATETIME NULL,
                estimated_hours DECIMAL(4,1) NOT NULL,
                status ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """

        # sessions
        TABLES["sessions"] = """
        CREATE TABLE IF NOT EXISTS sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_id INT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            duration_minutes INT NOT NULL,
            session_type VARCHAR(100) NOT NULL,
            CONSTRAINT fk_sessions_task
                FOREIGN KEY (task_id)
                REFERENCES tasks(id)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        # reflections
        TABLES["reflections"] = """
        CREATE TABLE IF NOT EXISTS reflections (
            id INT AUTO_INCREMENT PRIMARY KEY,
            week_start DATE NOT NULL,
            week_end DATE NOT NULL,
            reflection_text TEXT NOT NULL
        ) ENGINE=InnoDB;
        """

        for name, ddl in TABLES.items():
            try:
                print(f"Creating table `{name}`...")
                self.cursor.execute(ddl)
                print(f"Table `{name}` is ready.")
            except mysql.connector.Error as e:
                print(f"Error creating table `{name}`: {e}")
                raise
        
    def main(self):
        # Step 1: Connect to server
        try:
            self.connect()
            self.create_db()
            self.create_tables()
        except mysql.connector.Error as e:
            print(f"Database: {e}")

if __name__ == "__main__":
    database_builder = DatabaseBuilder()
    database_builder.main()
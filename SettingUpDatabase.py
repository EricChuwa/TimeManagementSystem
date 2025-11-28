import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() # Loads the env fil



class DatabaseBuilder:
    def __init__(self):
        self.config = {
            'host' : os.getenv('DB_HOST'),
            'user' : os.getenv('DB_USER'),
            'password' : os.getenv('DB_PASS'),
            'database' : os.getenv('DB_NAME'),
            'port': int(os.getenv("DB_PORT")),
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
    

test = DatabaseBuilder()
test.connect()
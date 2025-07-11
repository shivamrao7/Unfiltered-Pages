import sqlite3
import os

DATABASE_FILE = "data/blog.db"

class User:
    def __init__(self, username, password):
        self.id = None
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

    @staticmethod
    def _init_db():
        """Initialize the database and create tables if they don't exist"""
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Create posts table if it doesn't exist (in case Post model hasn't been used yet)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                author TEXT NOT NULL,
                is_published BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    @staticmethod
    def _get_connection():
        """Get database connection"""
        User._init_db()
        return sqlite3.connect(DATABASE_FILE)

    @staticmethod
    def load_users():
        """Load all users from database"""
        conn = User._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        users = []
        
        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "created_at": row[3]
            })
        
        conn.close()
        return users

    @staticmethod
    def save_user(user):
        """Save a new user to database"""
        conn = User._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (user.username, user.password))
            
            user.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            conn.close()
            return False

    @staticmethod
    def find_user(username):
        """Find a user by username"""
        conn = User._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "created_at": row[3]
            }
        return None

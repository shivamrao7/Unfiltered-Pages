import sqlite3
import os
from datetime import datetime

DATABASE_FILE = "data/blog.db"

class Post:
    def __init__(self, title, body, author, is_published=False):
        self.id = None
        self.title = title
        self.body = body
        self.author = author
        self.is_published = is_published
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author": self.author,
            "is_published": self.is_published,
            "created_at": self.created_at
        }

    @staticmethod
    def _init_db():
        """Initialize the database and create tables if they don't exist"""
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()

    @staticmethod
    def _get_connection():
        """Get database connection"""
        Post._init_db()
        return sqlite3.connect(DATABASE_FILE)

    @staticmethod
    def load_all():
        """Load all posts from database"""
        conn = Post._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')
        posts = []
        
        for row in cursor.fetchall():
            posts.append({
                "id": row[0],
                "title": row[1],
                "body": row[2],
                "author": row[3],
                "is_published": bool(row[4]),
                "created_at": row[5]
            })
        
        conn.close()
        return posts

    @staticmethod
    def save(post):
        """Save a new post to database"""
        conn = Post._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (title, body, author, is_published, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (post.title, post.body, post.author, post.is_published, post.created_at))
        
        post.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_id(post_id):
        """Find a post by ID"""
        conn = Post._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "body": row[2],
                "author": row[3],
                "is_published": bool(row[4]),
                "created_at": row[5]
            }
        return None

    @staticmethod
    def update(post_id, updated_data):
        """Update a post in database"""
        conn = Post._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE posts 
            SET title = ?, body = ?, is_published = ?
            WHERE id = ?
        ''', (
            updated_data["title"],
            updated_data["body"],
            updated_data["is_published"],
            post_id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def get_by_status(is_published=True):
        """Get posts by publication status"""
        conn = Post._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM posts WHERE is_published = ? ORDER BY created_at DESC', (is_published,))
        posts = []
        
        for row in cursor.fetchall():
            posts.append({
                "id": row[0],
                "title": row[1],
                "body": row[2],
                "author": row[3],
                "is_published": bool(row[4]),
                "created_at": row[5]
            })
        
        conn.close()
        return posts

#!/usr/bin/env python3
"""
Migration script to transfer data from JSON files to SQLite database
"""

import json
import os
import sqlite3
from datetime import datetime

def migrate_posts():
    """Migrate posts from JSON to SQLite"""
    posts_file = "data/posts.json"
    db_file = "data/blog.db"
    
    if not os.path.exists(posts_file):
        print("No posts.json file found. Skipping posts migration.")
        return
    
    # Read existing posts from JSON
    with open(posts_file, 'r') as f:
        posts_data = json.load(f)
    
    # Initialize database
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create posts table
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
    
    # Check if posts table is empty
    cursor.execute('SELECT COUNT(*) FROM posts')
    if cursor.fetchone()[0] > 0:
        print("Posts table already has data. Skipping posts migration.")
        conn.close()
        return
    
    # Insert posts from JSON
    for post in posts_data:
        cursor.execute('''
            INSERT INTO posts (id, title, body, author, is_published, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            post['id'],
            post['title'],
            post['body'],
            post['author'],
            post['is_published'],
            post['created_at']
        ))
    
    conn.commit()
    conn.close()
    print(f"Migrated {len(posts_data)} posts to SQLite database.")

def migrate_users():
    """Migrate users from JSON to SQLite"""
    users_file = "data/users.json"
    db_file = "data/blog.db"
    
    if not os.path.exists(users_file):
        print("No users.json file found. Skipping users migration.")
        return
    
    # Read existing users from JSON
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    # Initialize database
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if users table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        print("Users table already has data. Skipping users migration.")
        conn.close()
        return
    
    # Insert users from JSON
    for user in users_data:
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (user['username'], user['password']))
        except sqlite3.IntegrityError:
            print(f"User {user['username']} already exists, skipping.")
    
    conn.commit()
    conn.close()
    print(f"Migrated users to SQLite database.")

def main():
    """Run the migration"""
    print("Starting migration from JSON to SQLite...")
    
    migrate_posts()
    migrate_users()
    
    print("Migration completed!")
    print("You can now delete the JSON files if you want:")
    print("- data/posts.json")
    print("- data/users.json")

if __name__ == "__main__":
    main() 
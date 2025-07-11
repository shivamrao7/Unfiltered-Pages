#!/usr/bin/env python3
"""
Database utility functions for the blog application
"""

import sqlite3
import os

DATABASE_FILE = "data/blog.db"

def init_database():
    """Initialize the database with tables"""
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
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
    print("Database initialized successfully!")

def show_database_stats():
    """Show database statistics"""
    if not os.path.exists(DATABASE_FILE):
        print("Database file does not exist!")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Count posts
    cursor.execute('SELECT COUNT(*) FROM posts')
    total_posts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM posts WHERE is_published = 1')
    published_posts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM posts WHERE is_published = 0')
    draft_posts = cursor.fetchone()[0]
    
    # Count users
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    print("=== Database Statistics ===")
    print(f"Total posts: {total_posts}")
    print(f"Published posts: {published_posts}")
    print(f"Draft posts: {draft_posts}")
    print(f"Total users: {total_users}")
    print("=========================")

def list_posts():
    """List all posts in the database"""
    if not os.path.exists(DATABASE_FILE):
        print("Database file does not exist!")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')
    posts = cursor.fetchall()
    
    conn.close()
    
    if not posts:
        print("No posts found in database.")
        return
    
    print("=== All Posts ===")
    for post in posts:
        status = "PUBLISHED" if post[4] else "DRAFT"
        print(f"ID: {post[0]} | {post[1]} | By: {post[3]} | Status: {status}")
        print(f"Created: {post[5]}")
        print("-" * 50)

def list_users():
    """List all users in the database"""
    if not os.path.exists(DATABASE_FILE):
        print("Database file does not exist!")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    
    conn.close()
    
    if not users:
        print("No users found in database.")
        return
    
    print("=== All Users ===")
    for user in users:
        print(f"ID: {user[0]} | Username: {user[1]} | Created: {user[3]}")
    print("-" * 30)

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python db_utils.py [command]")
        print("Commands:")
        print("  init     - Initialize database")
        print("  stats    - Show database statistics")
        print("  posts    - List all posts")
        print("  users    - List all users")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        init_database()
    elif command == "stats":
        show_database_stats()
    elif command == "posts":
        list_posts()
    elif command == "users":
        list_users()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 
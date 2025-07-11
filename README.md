# Blog Application

A modern Flask-based blogging application with user authentication and SQLite database storage.

## Features

- **User Authentication**: Sign up, login, and logout functionality
- **Blog Post Management**: Create, edit, and publish blog posts
- **Draft System**: Save posts as drafts before publishing
- **Responsive Design**: Modern, mobile-friendly UI
- **SQLite Database**: Robust data storage with SQLite
- **Session Management**: Secure user sessions

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

## Database Migration

If you have existing JSON data, run the migration script to transfer it to SQLite:

```bash
python migrate_to_sqlite.py
```

## Database Utilities

Use the database utility script to manage the database:

```bash
# Initialize database
python db_utils.py init

# Show database statistics
python db_utils.py stats

# List all posts
python db_utils.py posts

# List all users
python db_utils.py users
```

## Project Structure

```
Blogging Project/
├── app.py                 # Main Flask application
├── controllers/           # Business logic
│   └── post_controller.py
├── models/               # Data models
│   ├── post.py
│   └── user.py
├── routes/               # Route handlers
│   ├── post_routes.py
│   └── user_routes.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── posts.html
│   ├── post_form.html
│   └── post_details.html
├── data/                 # Database and data files
│   └── blog.db
├── migrate_to_sqlite.py  # Migration script
└── db_utils.py          # Database utilities
```

## Usage

### For Users
1. **Sign Up**: Create a new account
2. **Login**: Access your account
3. **View Posts**: Browse published blog posts
4. **Create Posts**: Write and publish your own posts
5. **Edit Posts**: Modify your existing posts
6. **Manage Drafts**: Save posts as drafts for later

### For Developers
- The application uses SQLite for data storage
- All templates extend `base.html` for consistent styling
- Session management handles user authentication
- Flash messages provide user feedback

## Database Schema

### Posts Table
- `id`: Primary key (auto-increment)
- `title`: Post title
- `body`: Post content
- `author`: Username of the author
- `is_published`: Boolean flag for published/draft status
- `created_at`: Timestamp of creation

### Users Table
- `id`: Primary key (auto-increment)
- `username`: Unique username
- `password`: User password
- `created_at`: Timestamp of account creation

## Security Features

- Session-based authentication
- Password protection for user accounts
- SQL injection prevention with parameterized queries
- CSRF protection through Flask-WTF

## Future Enhancements

- Password hashing with bcrypt
- Email verification
- Rich text editor for posts
- Image upload functionality
- Comment system
- User roles and permissions
- Search functionality
- RSS feeds 
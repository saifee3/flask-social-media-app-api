# 🛋️ Social Media Application
<img src="https://github.com/user-attachments/assets/b9d2baed-49f2-4feb-a385-2fc01c298b28" alt="Custom Icon" width="1050" height="300">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0.0-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-red)

## Table of Contents
- [Project Overview](#project-overview) 🌟
- [Features](#features) ✨
- [Technologies](#technologies) ⚙️
- [Installation](#installation) 💻
- [Usage](#usage) 🚀
- [API Documentation](#api-documentation) 📘
- [Folder Structure](#folder-structure) 📂
- [Contributing](#contributing) 🤝
- [License](#license) 📜
- [Credits](#credits) 🙏

## Project Overview 🌟

This social media application is designed to provide a robust platform for user interaction and content sharing. It implements modern web development practices and follows RESTful principles for its API design. The application is built with security in mind, using JWT authentication and password hashing to protect user data.

## Features ✨

- **User Management**:
  - 📝 Registration with email verification
  - 🔑 Login with JWT authentication
  - 📋 Profile management (update personal information)

- **Post Management**:
  - 📝 Create, read, update, and delete posts

- **Commenting System**:
  - 📌 Add, edit, and delete comments

- **Like System**:
  - ❤️ Like/unlike posts
  - 📊 View who liked a post
  - 📈 Like analytics

- **Security**:
  - 🔐 JWT-based authentication
  - 🗝️ Password hashing with Bcrypt

## Technologies ⚙️

- **Backend**: 🐍 Python 3.8+, 🌐 Flask 2.0.0
- **Database**: 🗄️ SQLite (easily switchable to PostgreSQL or MySQL)
- **Authentication**: 🔑 Flask-JWT-Extended
- **Password Hashing**: 🗑️ Flask-Bcrypt
- **CORS Support**: 🌐 Flask-CORS
- **API Documentation**: 📘 Postman

## Installation 💻

### Prerequisites
- Python 3.8 or higher
- Git
- Basic command-line knowledge

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/social-media-app.git
   cd social-media-app
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   SQLALCHEMY_DATABASE_URI=sqlite:///My_Database_user_22.db
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

## Usage 🚀

### User Registration
```bash
POST /user/signup
```
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### User Login
```bash
POST /user/login
```
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Creating a Post
After login, use the received JWT token to create a post:
```bash
POST /post/
```
```json
{
  "title": "My First Post",
  "content": "This is the content of my first post.",
  "media_url": "https://example.com/image.jpg"
}
```

### Updating a Post
```bash
PUT /post/<post_id>
```
```json
{
  "title": "Updated Title",
  "content": "Updated content of my post."
}
```

### Deleting a Post
```bash
DELETE /post/<post_id>
```

## API Documentation 📘

### User Endpoints
- `POST /user/signup` - User registration
- `POST /user/login` - User login
- `GET /user/profile` - Get current user's profile (JWT required)
- `PUT /user/profile` - Update user profile (JWT required)
- `PATCH /user/profile` - Partially update user profile (JWT required)
- `DELETE /user/profile` - Delete user account (JWT required)

### Post Endpoints
- `POST /post/` - Create a new post (JWT required)
- `GET /post/` - Get all posts
- `GET /post/my-posts` - Get current user's posts (JWT required)
- `GET /post/<post_id>` - Get a specific post
- `PUT /post/<post_id>` - Update a post (JWT required)
- `PATCH /post/<post_id>` - Partially update a post (JWT required)
- `DELETE /post/<post_id>` - Delete a post (JWT required)

### Comment Endpoints
- `POST /comment/post/<post_id>` - Add comment to a post (JWT required)
- `GET /comment/post/<post_id>` - Get comments for a post
- `PUT /comment/update/<comment_id>` - Update a comment (JWT required)
- `DELETE /comment/<comment_id>` - Delete a comment (JWT required)

### Like Endpoints
- `POST /like/post/<post_id>` - Like a post (JWT required)
- `GET /like/post/<post_id>` - Get likes for a post
- `DELETE /like/post/<post_id>` - Unlike a post (JWT required)

## Folder Structure 📂

```
social_media_app/
│
├── app.py              # Main application file
├── models.py           # Database models
├── requirements.txt    # Project dependencies
├── README.md           # This documentation file
├── LICENSE             # Project license
│
└── routes/             # Route definitions
    ├── __init__.py
    ├── user_routes.py  # User authentication routes
    ├── post_routes.py  # Post creation and management routes
    ├── comment_routes.py # Comment routes
    └── like_routes.py  # Like routes

```


## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits 🙏

- **Python Development Community**
- **Flask Development Team** - [@pallets](https://github.com/pallets/flask)
- **SQLite Development Team** - [sqlite.org](https://www.sqlite.org)


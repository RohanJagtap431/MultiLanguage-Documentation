# 🌐 MultiLanguage Documentation

A multilingual documentation platform built with Django to provide structured programming guides, tutorials, and learning resources in multiple languages.

## 🚀 Live Demo

**Website:** https://multilanguage-documentation.onrender.com/

**GitHub Repository:** https://github.com/RohanJagtap431/MultiLanguage-Documentation

## 📌 About The Project

MultiLanguage Documentation is a web-based learning platform designed to make programming documentation accessible to learners through a structured and multilingual experience.

The project uses Django for backend development and provides user registration and login functionality.

## ✨ Features

- User Registration
- User Login
- Django-based backend
- Structured documentation platform
- Multilingual learning platform
- Responsive web interface
- PostgreSQL database integration
- Secure environment-based configuration

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Django | Web Framework |
| HTML | Page Structure |
| CSS | Styling |
| JavaScript | Frontend Interactions |
| PostgreSQL | Database |
| Neon | Cloud Database Hosting |
| Render | Web Application Hosting |
| Git & GitHub | Version Control |

## 📂 Project Structure

```text
MultiLanguage-Documentation/
│
├── accounts/
├── config/
├── documentation/
├── static/
├── templates/
│
├── .gitignore
├── manage.py
└── requirements.txt
```

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/RohanJagtap431/MultiLanguage-Documentation.git
```

### 2. Open Project Folder

```bash
cd MultiLanguage-Documentation
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

For PostgreSQL, configure `DATABASE_URL` with your database connection string.

### 7. Apply Migrations

```bash
python manage.py migrate
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Open in your browser:

http://127.0.0.1:8000/

## 🌍 Deployment

The application is deployed using:

- **Web Hosting:** Render
- **Database Hosting:** Neon PostgreSQL

Live URL: https://multilanguage-documentation.onrender.com/

## 🔐 Security

- Environment variables for sensitive configuration
- Secret keys are not stored in source code
- Production debug mode disabled
- HTTPS security settings
- Environment-based database configuration

## 👨‍💻 Developer

**Rohan Jagtap**

- GitHub: https://github.com/RohanJagtap431

## 📄 License

This project is currently available for educational and learning purposes. No separate open-source license has been specified.

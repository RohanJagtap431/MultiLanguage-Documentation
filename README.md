# 🌐 MultiLanguage Documentation

**A Multilingual Documentation, Developer Learning & Examination Platform**

MultiLanguage Documentation is a Django-based web application designed to help students and developers learn programming through structured documentation, interactive coding challenges, and an online examination system.

The platform combines programming tutorials, debugging practice, performance tracking, student examinations, and ranking features in one place.

## 🔗 Project Links

🌍 **Live Website:** https://multilanguage-documentation.onrender.com/

💻 **GitHub Repository:** https://github.com/RohanJagtap431/MultiLanguage-Documentation

---

## 🚀 Overview

MultiLanguage Documentation provides an organized learning environment where students can explore programming documentation, practice debugging, participate in coding challenges, and attempt online examinations.

The platform includes user authentication, documentation management, coding games, performance tracking, examination management, result evaluation, and student rankings.

## ✨ Features

### 📚 1. Documentation System

- Structured programming documentation.
- Organized learning resources and tutorials.
- Multilingual learning experience.
- Easy navigation between topics.

### 👤 2. User Authentication

- User registration and login.
- Custom user authentication system.
- User-specific platform access.

### 🕵️ 3. Code Detective

An interactive coding challenge module designed to improve programming and debugging skills.

- Bug Hunter Mode.
- Mixed Challenge Mode.
- Multiple programming languages.
- Easy, Medium, and Hard difficulty levels.
- 10 questions per challenge.
- 10-minute countdown timer.
- Automatic score calculation.
- Result and performance summary.

### 🏆 4. Leaderboard & Ranking

- Global player leaderboard.
- Player XP and ranking system.
- Games played statistics.
- Correct answers tracking.
- Personal rank display.
- Recent game results.

### 📊 5. Performance Tracking

- Total XP tracking.
- Games played.
- Correct answers.
- Accuracy calculation.
- Individual game results.

### 📝 6. Online Examination System

A student examination module for conducting subject-wise programming examinations.

- Class and subject management.
- Topic-wise question bank.
- MCQ, short-answer, and long-answer questions.
- Different examination formats: 20, 30, and 40 marks.
- Configurable examination duration.
- Random question paper generation.
- Online examination submission.
- Automatic MCQ evaluation.
- Written answer evaluation with AI assistance.
- Examination result management.
- Admin result approval workflow.

### 📄 7. My Examination Results

Students can track their examination history through a dedicated results dashboard.

- Total examinations attempted.
- Approved results count.
- Pending approval count.
- Rejected results count.
- Subject-wise examination details.
- Obtained marks and percentage.
- Examination submission date.
- Detailed result view.

### 🥇 8. Class Ranking System

A ranking system to compare student examination performance.

- Class overall ranking.
- Subject-wise ranking.
- Top 3 student podium.
- Top 50 student leaderboard.
- Percentage-based ranking.
- Equal ranks for students with the same percentage.
- Ranking based on available examination results.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| Django ORM | Database operations |
| PostgreSQL | Database |
| SQLite | Local development database |
| HTML5 | Frontend structure |
| CSS3 | Styling and responsive UI |
| JavaScript | Interactive functionality |
| Django Templates | Dynamic frontend |
| Groq API | AI-assisted written answer evaluation |
| Git & GitHub | Version control |
| Render | Deployment |

## 📂 Project Structure

```text
MultiLanguage-Documentation/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── documentation/
│
├── bug_hunter/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── examination/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│
├── static/
│   └── css/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/RohanJagtap431/MultiLanguage-Documentation.git
```

### 2. Navigate to Project Folder

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

Create a `.env` file in the project root and configure the required environment variables.

Example:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=openai/gpt-oss-120b
```

Configure your database connection if you are using PostgreSQL.

**Important:** Never upload your actual `.env` file, database credentials, or API keys to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Create Superuser

```bash
python manage.py createsuperuser
```

### 9. Start Development Server

```bash
python manage.py runserver
```

Open your browser:

http://127.0.0.1:8000/

---

## 🎯 Project Objectives

- Make programming documentation easier to understand.
- Provide an interactive coding learning experience.
- Improve debugging and problem-solving skills.
- Track coding performance through XP and rankings.
- Conduct online programming examinations.
- Evaluate student examination performance.
- Provide subject-wise and overall student rankings.
- Build a useful learning platform for students and developers.

## 🔮 Future Enhancements

- AI-powered learning assistant.
- Online code playground.
- API testing laboratory.
- Personal learning roadmap.
- Developer community.
- Smart learning analytics.
- AI-based documentation assistance.

---

## 👨‍💻 Developer

**Rohan Chandrakant Jagtap**

Python & Django Backend Developer

- **GitHub:** https://github.com/RohanJagtap431
- **Repository:** https://github.com/RohanJagtap431/MultiLanguage-Documentation
- **Live Website:** https://multilanguage-documentation.onrender.com/

---

⭐ If you find this project useful, consider giving the repository a star!

**Built with Python & Django.**

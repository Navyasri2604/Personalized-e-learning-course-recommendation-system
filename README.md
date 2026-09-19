# AI-Powered Personalized Learning and Skill Development Platform

A complete, production-ready web application built with Django that provides intelligent course recommendations based on user profiles.

## Features
- **Smart Registration & Profiles**: Users can enter their skills, interests, and career goals.
- **Machine Learning Recommendations**: Uses TF-IDF and Cosine Similarity to recommend the best courses.
- **Career Roadmaps**: Automatically generates step-by-step career roadmaps for roles like AI Engineer, Data Scientist, etc.
- **Progress Tracking & Analytics**: Users can track their course status and view visual analytics using Chart.js.
- **Premium UI**: Designed with Bootstrap 5, Glassmorphism, and a modern color palette.
- **Automated Data Seeding**: Includes a management script to automatically generate 500+ realistic courses without external datasets.

## Technologies Used
- **Backend**: Python, Django 3.2+
- **Machine Learning**: Pandas, NumPy, Scikit-Learn
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Database**: SQLite3

## Installation and Setup

1. **Clone the repository** (if using Git):
   ```bash
   git clone <repo_url>
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate the database with courses**:
   ```bash
   python manage.py seed_data
   ```

6. **Create an admin user**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to `http://127.0.0.1:8000/`.

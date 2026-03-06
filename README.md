# Next Gen Blog

## Overview
Next Gen Blog is a modern blogging application built with Django. It allows users to create, edit, and manage their blog posts with ease.

## Features
- User authentication
- Rich text editor for post content
- Categories and tags for organizing posts
- Commenting system
- Responsive design

## Requirements
- Python 3.6+
- Django 3.0+
- PostgreSQL (or other supported database)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/JsamsIvyTech/Next_Gen_Blog.git
   cd Next_Gen_Blog
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Configure your database settings in `settings.py`.
   - Run migrations:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage
- Navigate to `http://127.0.0.1:8000` to access the application.
- For admin access, go to `http://127.0.0.1:8000/admin`.

## Contribution
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
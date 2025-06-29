# BE-Capstone-Project

## Overview

BE-Capstone-Project is a Django-based web application . This project utilizes modern web technologies and best practices to ensure a robust and scalable application.

## Features

- User registration and authentication
- RESTful API endpoints for data management
- Cross-Origin Resource Sharing (CORS) support
- JWT authentication for secure API access
- Static file serving with Whitenoise
- [Add any other features specific to your project]

## Technologies Used

- **Django**: The web framework used for building the application.
- **Django REST Framework**: For creating RESTful APIs.
- **MySQL**: Database management system for data storage.
- **Whitenoise**: Middleware for serving static files in production.
- **Python**: Programming language used for development.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Osamaseid/BE-Capstone-Project.git
   cd BE-Capstone-Project
   ```
2. **Create a virtual environment**:

```bash
 python3 -m venv venv
 source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Install dependencies**:

```bash
 pip install -r requirements.txt
```

4. **Set up the database**:

```bash
  Update your database settings in settings.py and run migrations:
  python manage.py migrate
```

5. **Collect static files**:

```bash
 python manage.py collectstatic
```

6. **Run the development server**:

```bash
python manage.py runserver
```

**Usage**

Access the API at http://localhost:8000/api/.
Use tools like Postman or cURL to interact with the API endpoints.
Contributing
Contributions are welcome! Please follow these steps to contribute:

**Fork the repository.**

Create a new branch (git checkout -b feature/AmazingFeature).
Make your changes and commit them (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.

**Acknowledgments**

Django Documentation
Django REST Framework Documentation
Whitenoise Documentation


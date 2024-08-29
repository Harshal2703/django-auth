# Django Authentication System

This project is a Django-based web application with user authentication functionalities, including login, signup, password management, and user profile features.

## Features

1. **User Authentication**: Users can sign in using their email or username along with a password.
2. **Login Page**: Allows users to log in using their email or username and password. Includes links to sign up and reset the password.
3. **Sign Up Page**: New users can register by providing a username, email, and password (with confirmation).
4. **Forgot Password Page**: Users can request a password reset by providing their email, which sends reset instructions.
5. **Change Password Page**: Authenticated users can change their password by providing the old password, new password, and confirmation of the new password.
6. **Dashboard**: Only accessible to authenticated users. Displays a greeting message and links to the profile and change password pages, along with a logout option.
7. **Profile Page**: Displays user information such as username, email, date joined, and last updated. Includes a logout option.

## Installation


   ```bash
    pip install django
    django-admin startproject myproject
    cd myproject
    python manage.py startapp myapp
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
   ```
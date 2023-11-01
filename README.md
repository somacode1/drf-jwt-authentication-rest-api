# Django REST API with JWT Authentication (Authentication API)

![poster](./static//imgs//poster.png)

We're going to take you step-by-step to build a fully functional open-source JWT Authentication REST API using Python, Django Rest Framework.

## Prerequisites

1. [Python==3.9.5 or Greater](https://python.org)
2. [Django==4.2.6 or Greater ](https://docs.djangoproject.com)
3. [djangorestframework==3.14.0](https://www.django-rest-framework.org/)
4. [PyJWT==2.7.0](https://pyjwt.readthedocs.io/en/stable/)

You can view all the dependencies from the [requirements.txt](./requirements.txt) file.

## Project Installation Instructions

1. Navigate to your workspace and create a virtual environment with `python -m venv env`

2. Activate the virtual environment

    - **Linux**: Activate the virtual environment run: `source .env/bin/activate`

    - **Windows**: Activate the virtual environment run: `env\Scipts\activate`

3. Install the following project dependencies run:

   ```bash
        pip install Django==4.2.6
        pip install djangorestframework==3.14.0
        pip install PyJWT==2.7.0
   ```

4. After the installation is complete let's create our [django project](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), we are going to call our project **core** run: `django-admin startproject core`. 
Let’s look at what startproject created:

    ```markdown
        core/
        manage.py
        core/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py
    ```

5. After the creation of the project, let's create an app called **users**. First you need to `cd` to the created project which is named **core** and run: `django-admin startapp users`. The application will be created inside the Django project **core**. Let's look at the folder structure below.

    ```markdown

            core/
            manage.py
            core/
                __init__.py
                settings.py
                urls.py
                asgi.py
                wsgi.py
            users/
                __init__.py
                admin.py
                apps.py
                migrations/
                    __init__.py
                models.py
                tests.py
                views.py
    ```

6. Navigate to`settings.py` and update the following:

    ```python
        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',  # NEW SET UP FOR DJANGO REST FRAMEWORK
        'users', # NEW ADD USERS APP IN THE INSTALLED APPS 
    ]

    # NEW ADD ALL OF THIS 
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'users.authentication.backends.JWTAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }
    ```

7. Let's create a file in the following directory in the **users** app [/users/authentication/backends.py](./users/authentication/backends.py). If you don't have the [authentication/](./users/authentication/) you MUST create it and also in the authentication folder add `__init__.py` file to make the module accessible.

8. The following code implements the [JWT middleware](./users/authentication/backends.py)

9. [Let's create our models in the user application](./users/models.py)

10. [Let's create our managers in the user application](./users/managers.py)

11. [Let's Implement the serializers](./users/serializers.py)

12. [Let's Implement the Views](./users/views.py)

13. [Let's Implement the user app URLS](./users/urls.py) and [core URL](./core/urls.py)

14. After that you need to run migrations to create the migration files run: `python manage.py makemigrations`

15. To apply the migrations and create the tables in the database run: `python manage.py migrate`

16. If you want to test the application you will find the tests at [users/tests.py](./users/tests.py) run tests: `python manage.py tests`

17. run the application `manage.py runserver`

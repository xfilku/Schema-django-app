#!/usr/bin/env python
"""
Management script for Django.

This script allows administrative tasks to be run in the context of the Django project.
Typically used to start the development server, run migrations, tests, and other Django commands.

Usage:
    python manage.py runserver
    python manage.py migrate
    python manage.py test
    ...
"""

import os
import sys

def main():
    """
    Entry point for Django administrative tasks.

    Sets the default settings module and delegates command-line execution
    to Django's management utility.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solution.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and "
            "available on your PYTHONPATH environment variable. "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

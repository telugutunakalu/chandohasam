# -*- coding: utf-8 -*-
"""WSGI entry point: ``gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app``."""
from padya_eval import create_app

app = create_app()

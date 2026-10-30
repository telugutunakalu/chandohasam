# -*- coding: utf-8 -*-
"""WSGI entry point: ``gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app``.

Study 1 at /, study 2 (data_study2/, the he2_ poems) at /study2, and the home page / choosing between them
(create_site, README §3a). Live since 2026-10-30.
"""
from padya_eval import create_site

app = create_site()

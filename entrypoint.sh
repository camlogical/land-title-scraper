#!/bin/bash
playwright install --with-deps
exec gunicorn app:app --bind 0.0.0.0:8080

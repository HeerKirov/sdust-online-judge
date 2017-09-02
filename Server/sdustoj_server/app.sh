#!/usr/bin/env bash
nohup gunicorn sdustoj_server.wsgi:application -b 0.0.0.0:8000 --reload >> gunicorn_log.log 2>&1 &
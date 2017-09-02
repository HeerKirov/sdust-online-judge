#!/usr/bin/env bash
nohup gunicorn sdustoj_client.wsgi:application -b 0.0.0.0:8008 --reload >> gunicorn_log.log 2>&1 &
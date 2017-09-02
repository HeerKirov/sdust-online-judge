#!/usr/bin/env bash
nohup python3 updater.py >> updater.log 2>&1 &
nohup python3 submission_updater.py >> submission_updater.log 2>&1 &
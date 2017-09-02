#!/usr/bin/env bash
nohup python3 problem_updater.py >> problem_updater.log 2>&1 &
nohup python3 submission_reporter.py >> submission_reporter.log 2>&1 &
nohup python3 submission_reptile.py >> submission_reptile.log 2>&1 &
nohup python3 submission_updater.py >> submission_updater.log 2>&1 &
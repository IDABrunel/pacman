#!/bin/bash
python3 wait_for_start.py
python3 run.py --style=default --arduino --logging --strategy=controller

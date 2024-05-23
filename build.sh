#!/bin/bash

# Create conda environment from env.yml file
conda env create -f env.yml

# Activate the created environment
conda activate netfix-env

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

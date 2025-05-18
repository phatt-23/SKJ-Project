# Stengah - SKJ-Project 

Basic github without git.

## Run the project

Run these commands:

```bash
# go to the working directory
cd stengah

# create virtual environment
python -m venv stengah_venv

# activate virtual environment
source stengah_venv/bin/activate        # bash
source stengah_venv/bin/activate.fish   # fish

# install dependencies
pip install django
pip install django-ninja
pip install pillow

# create migration and migrate (project uses sqlite3)
python manage.py makemigrations
python manage.py migrate

# run the web application
python manage.py runserver
```



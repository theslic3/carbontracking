# carbontracking

-> Download Requirements by running pip3 install -r requirements.txt

-> To run the app: go to main.py, and run through command line (path/to/carbontracking -> python3 main.py)
    or through IDE.

-> init.py -> initialisation for all components and connects auth and routes through blueprinting
-> auth.py contains routing for authentication
-> views.py contains routing for feature functionality
-> models.py contains the classes to be used by SQLAlchemy ORM
-> templates contains the various HTML template, with associated scripts, stylesheets and media stored in templates/static
-> database is stored in carbontracking/instance/database.db and is a sqlite database.

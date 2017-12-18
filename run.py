"""
Create a Flask app using an app factory and runs it.

Available functions:
- create_tables:  Runs before the first request.  Tells SQLAlchemy to
      create all the database tables.
"""

from app import create_app
from db import db

app = create_app('development')
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()

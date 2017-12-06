from app import create_app
from db import db

app = create_app('development')
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.run(port=5000)

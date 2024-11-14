import sqlalchemy as sa
import sqlalchemy.orm as so
from darts4dorks import app, db
from darts4dorks.models import User, Session


# Defines commands in 'flask shell' REPL
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Session': Session}


if __name__ == '__main__':
    app.run(debug=True)
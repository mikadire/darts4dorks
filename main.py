import sqlalchemy as sa
import sqlalchemy.orm as so
from darts4dorks import app


# Defines commands in 'flask shell' REPL
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so}


if __name__ == '__main__':
    app.run(debug=True)
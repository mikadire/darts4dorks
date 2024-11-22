import sqlalchemy as sa
import sqlalchemy.orm as so
from darts4dorks import create_app

app = create_app()


# Defines commands in 'flask shell' REPL
@app.shell_context_processor
def make_shell_context():
    return {"sa": sa, "so": so}

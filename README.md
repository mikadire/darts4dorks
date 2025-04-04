# Darts4Dorks

**darts4dorks** is a Flask-based web application designed for tracking your darts progress. This project was created for learning purposes and serves as part of my portfolio to showcase backend development skills.

## Features

- User authentication and session management
- Game tracking with player score history and interactive charts
- Database integration using SQLAlchemy
- Responsive UI with Bootstrap 5
- Email support

## Tech Stack

- **Backend:** Flask, SQLAlchemy
- **Frontend:** Bootstrap 5
- **Database:** MySQL or SQLite
- **Deployment:** Gunicorn, Nginx, Docker

## Installation

### Prerequisites

Ensure you have Python 3.x installed.

### Setup

1. Clone the repository:

```sh
git clone https://github.com/yourusername/darts4dorks.git
cd darts4dorks
```

2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Set up the database:

```sh
flask db upgrade
```

5. Run the application locally:

```sh
flask run
```

6. Navigate to `http://127.0.0.1:5000/` to access the app.

### Running with Docker

The above setup runs the application on a builtin development server and a SQLite database. In production, we will use the more robust Gunicorn server and MySQL databse inside Docker containers.

1. Install Docker

2. Create a `.env` file in the project root and configure the following variables:

```sh
SECRET_KEY=<secret-key>
DATABASE_URL=mysql+pymysql://<db-username>:<db-password>@mysql/darts4dorks
MYSQL_DATABASE=darts4dorks
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_USER=<db-username>
MYSQL_PASSWORD=<db-password>
```

For email support:

```sh
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_TLS=
MAIL_USERNAME=
MAIL_PASSWORD=
```

3. Run the application using Docker Compose:

   ```sh
   sudo docker compose up -d
   ```

4. The application will be accessible at `http://127.0.0.1:8000/`.

### Deployment

To deploy to production, install a web server such as nginx and point it to http://127.0.0.1:8000/.
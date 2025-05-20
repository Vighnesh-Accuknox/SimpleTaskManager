A basic Task Management app where users can:
- Create accounts (register/login)
- Create/update/delete tasks (title, description, deadline, status: pending/ongoing/completed)
- Each task is assigned to a "project"
- Background reminders (using Celery and Redis) for upcoming deadlines
- Auto-notifications sent (using Signals) when a task status changes
- REST APIs using DRF + JWT Authentication
- Admin panel for managing users, tasks, and projects
- Some basic filtering APIs (e.g., tasks by status, due date, assigned project)

To Start the project
```bash
#create a virtualenv
python -m venv .venv

#clone the repo
git clone repo-url

#activate the virtual environment
.\.venv\Scripts\activate

#install the dependencies
pip install -r requirements.txt

#run the migrations
python manage.py makemigrations project
python manage.py migrate

#run the server
python manage.py runserver

```

Routes - 
| Method   | URL               | Action           | Description            |
| -------- | ----------------- | ---------------- | ---------------------- |
| `GET`    | `/projects/`      | `list`           | Get all projects       |
| `POST`   | `/projects/`      | `create`         | Create a new project   |
| `GET`    | `/projects/{id}/` | `retrieve`       | Get a single project   |
| `PUT`    | `/projects/{id}/` | `update`         | Update a project       |
| `DELETE` | `/projects/{id}/` | `destroy`        | Delete a project       |
| `POST`   |  `/login`         | `login`          | User Login             |
| `POST`   |  `/signup`        | `signup`         | User Signup            |
| `GET`    | `/tasks/`         | `list`           | Get all task           |
| `POST`   | `/tasks/`         | `create`         | Create a new task      |
| `GET`    | `/tasks/{id}/`    | `retrieve`       | Get a single task      |
| `PUT`    | `/tasks/{id}/`    | `update`         | Update a task          |
| `DELETE` | `/tasks/{id}/`    | `destroy`        | Delete a task          |


# Async Task Management using Celery

1. ## Using Shell for Checking Deadlines Manually

```bash
#Start the Virtual Environment
.\.venv\Scripts\Activate

# start the shell
python manage.py shell

# In the shell
from project.tasks import send_upcoming_deadline_reminders
send_upcoming_deadline_reminders.delay()


```

Start the worker

```bash
# open the new terminal

#Start the Virtual Environment
.\.venv\Scripts\Activate

# run the celery worker command
celery -A assignment worker --loglevel=info --pool=solo
```

2. Using celery beat for Task Scheduling automatically

```bash
#Start the Virtual Environment
.\.venv\Scripts\Activate

# Run the Celery Beat
celery -A assignment beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Start the worker
```bash
# open the new terminal

#Start the Virtual Environment
.\.venv\Scripts\Activate

# run the celery worker command
celery -A assignment worker --loglevel=info --pool=solo
```

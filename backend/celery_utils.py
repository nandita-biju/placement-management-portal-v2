from celery import Celery, Task
from celery.schedules import crontab


def make_celery(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    broker = "redis://localhost:6379/0"
    backend = "redis://localhost:6379/0"

    # Read the UPPERCASE keys that Flask actually loaded from Config
    celery_app = Celery(
        app.import_name,
        broker=broker,
        backend=backend,
        task_cls=FlaskTask
    )

    celery_app.conf.update(app.config)

    # Explicitly set the Celery-native lowercase keys to guarantee
    # they are not overridden by conf.update or left as defaults
    celery_app.conf.broker_url = broker
    celery_app.conf.result_backend = backend

    celery_app.conf.timezone = "Asia/Kolkata"

    celery_app.conf.beat_schedule = {

        "daily-reminder-email": {
            "task": "tasks.reminder_tasks.send_daily_reminders",
            "schedule": crontab(hour=9, minute=0),
        },

        "monthly-report": {
            "task": "tasks.report_tasks.send_monthly_report",

            # FOR TESTING ONLY
            "schedule": crontab(hour=18, minute=35),
        },

    }

    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
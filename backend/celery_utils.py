from celery import Celery, Task

def make_celery(app):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(
        app.import_name,
        backend=app.config.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
        broker=app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        task_cls=FlaskTask
    )
    celery_app.conf.update(app.config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

from celery import Celery, Task
from celery.schedules import crontab

class CeleryConfig:
    broker_url = 'redis://localhost:6379/0'
    result_backend  = 'redis://localhost:6379/1'
    timezone = 'Asia/Kolkata'
    enable_utc = True

    # beat_schedule = {
    #     'daily_appt_notifications': {
    #         'task': 'appt_notify',
    #         'schedule': crontab(hour=7, minute=0),
    #     },
    #     'monthly_reports_email': {
    #         'task': 'monthly_report_all',
    #         'schedule': crontab(hour=8, minute=0, day_of_month='1'),
    #     },
    # }

    beat_schedule = {
        'daily_appt_notifications': {
            'task': 'appt_notify',
            'schedule': crontab(minute='*/3'),
        },
        'monthly_reports_email': {
            'task': 'monthly_report_all',
            'schedule': crontab(minute='*/3'),
        },
    }

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
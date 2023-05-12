from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import printhello

scheduler = BackgroundScheduler()

scheduler.add_job(printhello, 'interval', seconds=3)

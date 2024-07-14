from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

db = SQLAlchemy()

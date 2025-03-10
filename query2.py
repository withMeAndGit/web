from sqlalchemy import false

from data.jobs import Jobs
from data import db_session

from datetime import datetime

db_session.global_init('database/mars_explorer.db')
session = db_session.create_session()

work = Jobs()
work.team_leader = 1
work.job = 'deployment of residential modules 1 and 2'
work.work_size = 15
work.collaborators = '2, 3'
work.start_date = datetime.now()
work.is_finished = false()

session.add(work)
session.commit()
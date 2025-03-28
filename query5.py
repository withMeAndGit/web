from data.users import User
from data.jobs import Jobs
from data import db_session

db_session.global_init(input())
session = db_session.create_session()

result = session.query(Jobs)

if result:
    job: Jobs
    need = max(job.collaborators.count(',') for job in result)
    out = set()

    for job in result:
        if job.collaborators.count(',') == need:
            out.add(session.query(User).where(User.id == job.team_leader).first())

    user: User
    print(*sorted(f'{user.name} {user.surname}' for user in out), sep='\n')
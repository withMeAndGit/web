from flask_restful import Resource, reqparse
from flask import jsonify, abort, Response

from data import db_session
from data.jobs import Jobs

from datetime import datetime

JOBS_COLUMNS = ('id', 'team_leader', 'job', 'work_size', 'collaborators',
                'start_date', 'end_date', 'is_finished')

parser = reqparse.RequestParser()
parser.add_argument('team_leader', type=int)
parser.add_argument('job', type=str)
parser.add_argument('work_size', type=int)
parser.add_argument('collaborators', type=str)
parser.add_argument('start_date', type=str, default=datetime.now())
parser.add_argument('end_date', type=str, required=False)
parser.add_argument('is_finished', type=bool, default=False)


def abort_if_job_not_found(job_id: int) -> None:
    session = db_session.create_session()
    job: type[Jobs] = session.query(Jobs).get(job_id)

    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobResource(Resource):
    @staticmethod
    def get(job_id: int) -> Response:
        abort_if_job_not_found(job_id)

        session = db_session.create_session()
        job: type[Jobs] = session.query(Jobs).filter(Jobs.id == job_id).first()

        return jsonify(
            job.to_dict(only=JOBS_COLUMNS)
        )

    @staticmethod
    def delete(job_id: int) -> Response:
        abort_if_job_not_found(job_id)

        session = db_session.create_session()
        job: type[Jobs] = session.query(Jobs).filter(Jobs.id == job_id).first()
        session.delete(job)
        session.commit()

        return jsonify({ 'status': 'success' })


class JobListResource(Resource):
    @staticmethod
    def get() -> Response:
        session = db_session.create_session()
        jobs: list[type[Jobs]] = session.query(Jobs).all()

        job: type[Jobs]
        return jsonify(
            [job.to_dict(
                only=JOBS_COLUMNS
            ) for job in jobs]
        )

    @staticmethod
    def post() -> Response:
        args: dict = parser.parse_args()

        session = db_session.create_session()
        job: Jobs = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            is_finished=args['is_finished']
        )
        session.add(job)
        session.commit()

        return jsonify({ 'id': job.id })